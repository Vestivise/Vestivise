"""
Django settings for Vestivise project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from keys import *
from django.core.urlresolvers import reverse

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_key

# SECURITY WARNING: don't run with debug turned on in production!

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = True
ALLOWED_HOSTS = ['app.vestivise.com', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_js_reverse',
    'dashboard',
    'data',
    'thomson',
    'humanResources',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Vestivise.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Vestivise.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

db = None

if DEBUG:

    db = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
else:
    db = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': dbName,
        'USER': dbUser,
        'PASSWORD': dbPassword,
        'HOST': dbHost,
        'PORT': dbPort,
    }

DATABASES = {
    'default': db
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    'staticfiles',
)

# Media root

MEDIA_ROOT = '/static/media/'
MEDIA_URL = '/static/media/'

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


LOGOUT_URL = 'home'


# Email setup

EMAIL_HOST = email_host
EMAIL_PORT = email_port
EMAIL_USE_TLS = email_use_tls
EMAIL_HOST_USER = email_host_user
EMAIL_HOST_PASSWORD = email_host_password
SERVER_EMAIL = email_host_user
SEND_BROKEN_LINK_EMAILS = True


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
        'exception_logs': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/vestivise_warn.log',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'exception_logs'],
            'level': 'ERROR',
            'propagate': True,
            },
        'dashboard.test': {
            'handlers': ['mail_admins', 'exception_logs'],
            'level': 'ERROR',
            'propagate': True,
        },
        'humanResources': {
            'handlers': ['mail_admins', 'exception_logs'],
            'level': 'ERROR',
            'propagate': True,
        },
        'data': {
            'handlers': ['mail_admins', 'exception_logs'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['mail_admins', 'exception_logs'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

ADMINS = (
  ('Raylen', 'raylen@vestivise.com'),
  ('Alex', 'alex@vestivise.com'),

)
