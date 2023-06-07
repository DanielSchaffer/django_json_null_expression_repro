from django.db.models import JSONField, Model


class ThisHasAJSONField(Model):
    data = JSONField(null=True, blank=True, default=dict)

