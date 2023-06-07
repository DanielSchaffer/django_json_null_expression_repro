import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.path.append(os.path.join(BASE_DIR, "django_json_null_expression_repro"))

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django",
    "django_mysql",
    "django_json_null_expression_repro"
]

SECRET_KEY = "hi"
DEBUG = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)


STATIC_ROOT = os.path.join(BASE_DIR, "django_at_iw/static")

STATIC_URL = "/static/"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "NAME": "django_json_null_expr_repro",
        "USER": "django_json_null_expr_repro",
        "PASSWORD": "testing123",
        "TEST": {"NAME": "django_json_null_expr_repro"},
    },
}
