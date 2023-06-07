from pytest import raises
from django.db.models import Case, CharField, F, IntegerField, Value, When
from django.db.models.functions import Coalesce
from django.test import TestCase

from django_json_null_expression_repro.models import ThisHasAJSONField


class DemoTests(TestCase):

    def setUp(self):
        ThisHasAJSONField.objects.create(data=dict(test=None))

    def test_repro(self):
        qs = ThisHasAJSONField.objects.annotate(
            test_direct_ref=F("data__test"),
            missing_key_direct_ref=F("data__missing_key"),

            # when a null value from a JSON lookup is referenced through an expression that defines an output_field, it
            # gets converted to the string "null"
            test_case_ref=Case(
                # this is a silly useless expression of course, just for demonstration
                When(id__isnull=True, then=F("test_direct_ref")),
                default=F("test_direct_ref"),
                output_field=CharField(),
            ),
            missing_key_case_ref=Case(
                When(id__isnull=True, then=F("missing_key_direct_ref")),
                default=F("missing_key_direct_ref"),
                output_field=CharField(),
            ),
        )
        obj = qs.first()

        assert obj.test_case_ref == "null"  # :(
        assert obj.missing_key_case_ref is None  # implicit "None" values seem to be okay?

        # this becomes a much larger problem when the field is supposed to be a nullable number
        qs_int = qs.annotate(
            test_case_ref_int=Case(
                When(id__isnull=True, then=F("test_direct_ref")),
                default=F("test_direct_ref"),
                output_field=IntegerField(null=True),
            )
        )

        with raises(ValueError):
            qs_int.first()

        # using Coalesce first doesn't help either
        qs_int = qs.annotate(
            safe_test_ref=Coalesce(F("test_direct_ref"), Value(None)),
            test_case_ref_int=Case(
                When(id__isnull=True, then=F("safe_test_ref")),
                default=F("safe_test_ref"),
                output_field=IntegerField(null=True),
            )
        )

        with raises(ValueError):
            qs_int.first()

        # the workaround is to wrap the value in a case statement that explicitly checks for the string "null" and then
        # reference *that* in the expression
        qs = qs.annotate(
            safe_test_ref=Case(
                When(
                    test_direct_ref=Value("null"),
                    then=None,
                ),
                default=F("test_direct_ref"),
            ),
            test_case_ref_int=Case(
                When(id__isnull=True, then=F("safe_test_ref")),
                default=F("safe_test_ref"),
                output_field=IntegerField(null=True),
            )
        )

        obj = qs.first()

        assert obj.test_case_ref_int is None


