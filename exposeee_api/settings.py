"""
Django settings for exposeee_api project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import sentry_sdk

from datetime import timedelta
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from pathlib import Path
from decouple import config
from dj_database_url import parse as dburl
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")]
)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "corsheaders",
    "core",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    "storages",
    "django_s3_storage",
    "rest_framework_simplejwt.token_blacklist",
    "test_without_migrations",
    "django_rq",
    "channels",
    "django_json_widget",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "exposeee_api.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "core/templates"),
        ],
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

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

WSGI_APPLICATION = "exposeee_api.wsgi.application"

ASGI_APPLICATION = "exposeee_api.asgi.application"

REDIS_URL = config(
    "CACHE_URL",
    default="redis://127.0.0.1:6379/0",
)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

default_dburl = "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")

database_default = config(
    "DATABASE_URL",
    default=default_dburl,
    cast=dburl,
)

# database_default["OPTIONS"] = {
#     "pool": True,
# }

DATABASES = {
    "default": database_default,
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

PATH_PASSWORD_VALIDATION = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": f"{PATH_PASSWORD_VALIDATION}.UserAttributeSimilarityValidator",
    },
    {
        "NAME": f"{PATH_PASSWORD_VALIDATION}.MinimumLengthValidator",
    },
    {
        "NAME": f"{PATH_PASSWORD_VALIDATION}.CommonPasswordValidator",
    },
    {
        "NAME": f"{PATH_PASSWORD_VALIDATION}.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

REST_USE_JWT = True

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

ACCOUNT_AUTHENTICATION_METHOD = "username_email"

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_EMAIL_SUBJECT_PREFIX = "MembaXMatch - "

ACCOUNT_ADAPTER = "core.adapter.CustomAccountAdapter"

ACCOUNT_SESSION_REMEMBER = True

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS", cast=lambda v: [s.strip() for s in v.split(",")]
)

CORS_ALLOW_HEADERS = list(default_headers) + [
    "content-disposition",
    "Access-Control-Allow-Credentials",
]

CORS_ALLOW_CREDENTIALS = True

#  Email
EMAIL_BACKEND = config("EMAIL_BACKEND")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_USE_TLS = config("EMAIL_USE_TLS")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("EMAIL_HOST_USER")


DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# The AWS region to connect to.
AWS_REGION = "fra1"

# The AWS access key to use.
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
# The AWS secret access key to use.
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "memba"

# The full URL to the S3 endpoint. Leave blank to use the default region URL.
AWS_S3_ENDPOINT_URL = "https://fra1.digitaloceanspaces.com"

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

AWS_LOCATION = "static"

# s3 static settings
if DEBUG:
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
else:
    STATIC_URL = "https://%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


# Sentry

SENTRY_DSN = config("SENTRY_DSN")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[
        DjangoIntegration(),
        RedisIntegration(),
    ],
    traces_sample_rate=0.8,
    send_default_pii=True,
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Use the same redis as with caches for RQ
RQ_QUEUES = {
    "default": {
        "USE_REDIS_CACHE": "default",
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
RQ_SHOW_ADMIN_LINK = True

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
