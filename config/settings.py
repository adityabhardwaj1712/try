import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "django_redis",
    "channels",
    "corsheaders",

    "apps.users",
    "apps.organizations",
    "apps.projects",
    "apps.tasks",
    "apps.comments",
    "apps.activity",
    "apps.notifications",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "common.middleware.organization_middleware.OrganizationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "frontend/templates"],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
            "apps.notifications.context_processors.unread_notifications",
        ],
    },
},
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
"default": {
"ENGINE": "django.db.backends.postgresql",
"NAME": os.getenv("POSTGRES_DB"),
"USER": os.getenv("POSTGRES_USER"),
"PASSWORD": os.getenv("POSTGRES_PASSWORD"),
"HOST": os.getenv("POSTGRES_HOST"),
"PORT": os.getenv("POSTGRES_PORT"),
}
}

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
"DEFAULT_AUTHENTICATION_CLASSES": [
"rest_framework_simplejwt.authentication.JWTAuthentication",
],
"DEFAULT_PERMISSION_CLASSES": [
"rest_framework.permissions.IsAuthenticated",
],
"DEFAULT_FILTER_BACKENDS": [
"django_filters.rest_framework.DjangoFilterBackend",
],
}

SIMPLE_JWT = {
"ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
"REFRESH_TOKEN_LIFETIME": timedelta(days=1),
"AUTH_HEADER_TYPES": ("Bearer",),
}

CACHES = {
"default": {
"BACKEND": "django_redis.cache.RedisCache",
"LOCATION": os.getenv("REDIS_URL"),
"OPTIONS": {
"CLIENT_CLASS": "django_redis.client.DefaultClient",
},
}
}

CHANNEL_LAYERS = {
"default": {
"BACKEND": "channels_redis.core.RedisChannelLayer",
"CONFIG": {
"hosts": [os.getenv("REDIS_URL")],
},
},
}


STATIC_URL = "/static/"

STATICFILES_DIRS = [
os.path.join(BASE_DIR, "frontend/static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"
LOGIN_URL = "/login/"

CORS_ALLOW_ALL_ORIGINS = True