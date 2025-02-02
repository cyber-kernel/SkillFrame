"""
Django settings for skillframe project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-x_zf(h-i#(0!1mqh)6k=c6fuevtx=5c*0ajsmcppd%!e9r@*v1"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# settings.py
LOGIN_URL = "/account/login/"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "account.apps.AccountConfig",
    "todo.apps.TodoConfig",
    "blog.apps.BlogConfig",
    "webhook.apps.WebhookConfig",
    "ckeditor",
    "tailwind",
    "theme",
    "django_browser_reload",
]
# required for tailwind

TAILWIND_APP_NAME = "theme"

# required for tailwind

INTERNAL_IPS = [
    "127.0.0.1",
]
# required for tailwind

NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "skillframe.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'webhook.context_processors.domain_name',
            ],
        },
    },
]

WSGI_APPLICATION = "skillframe.wsgi.application"


DOMAIN_NAME = "https://skillframe.org"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "static"


MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# CKEditor Settings
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = "//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",  # Full toolbar with all features
        "width": "auto",  # Auto width for responsiveness
        "height": 300,  # Optional: set desired editor height
        "extraPlugins": ",".join(
            [
                "codesnippet",  # Include extra plugins like Code Snippet if needed
            ]
        ),
        "allowedContent": True,  # Allow all HTML content
        "forcePasteAsPlainText": False,  # Keep HTML structure when pasting content
        "entities": False,  # Prevent encoding HTML entities like < and >
    },
}
