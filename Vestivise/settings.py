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
import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_key

# SECURITY WARNING: don't run with debug turned on in production!

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = config.debug
ALLOWED_HOSTS = ['localhost', '127.0.0.1', config.allowed_hosts, '286eee4a.ngrok.io']


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
    'humanResources',
    'import_export',
    'custom_user',
    'raven.contrib.django.raven_compat',
]


MIDDLEWARE_CLASSES = [
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Vestivise.urls'

AUTH_USER_MODEL = 'custom_user.EmailUser'


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

# Rest framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}

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
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



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
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'json': {
            'format': '{ "loggerName":"%(name)s", '
                      '"asciTime":"%(asctime)s", '
                      '"fileName":"%(filename)s", '
                      '"logRecordCreationTime":"%(created)f", '
                      '"functionName":"%(funcName)s", '
                      '"levelNo":"%(levelno)s", '
                      '"lineNo":"%(lineno)d", '
                      '"time":"%(msecs)d", '
                      '"levelName":"%(levelname)s", '
                      '"message":"%(message)s"}',
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
        'null': {
            'class': 'logging.NullHandler',
        },
        'sentry': {
            'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'loggly' : {
            'class': 'loggly.handlers.HTTPSHandler',
            'formatter': 'json',
            'level': 'INFO',
            'url': 'https://logs-01.loggly.com/inputs/8cd98d56-ebe7-40a1-9700-1cec2d672c8d/tag/python'
        }
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'nightly_process' : {
            'handlers' : ['loggly', 'console'],
            'level' : 'INFO',
            'propagate' : True
        },
        'algos' : {
            'handlers' : ['loggly', 'console'],
            'level' : 'INFO',
            'propagate' : True
        },
        'quovo_sync' : {
            'handlers' : ['loggly', 'console'],
            'level' : 'INFO',
            'propagate' : True
        },
        'instant_link' : {
            'handlers' : ['loggly', 'console'],
            'level' : 'INFO',
            'propagate' : False
        },
    }
}

ADMINS = (

)

OPERATIONS = (
    "josh@vestivise.com",
)

#CELERY STUFF
CELERY_TIMEZONE = 'UTC'
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

#RAVEN CONFIG
if not DEBUG:
    import raven

    RAVEN_CONFIG = {
        'dsn': 'https://fae4de274ae9455caaf93419086e3f90:9d7c5e14d36e43b4b355acf31c9b777a@sentry.io/140820',
        # If you are using git, you can also automatically configure the
        # release based on the git info.
        'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
    }

    CELERYD_HIJACK_ROOT_LOGGER = False
    LOGGING['loggers']['raven'] = {
         'level': 'DEBUG',
         'handlers': ['console'],
         'propagate': False,
     }
    LOGGING['loggers']['sentry.errors'] = {
         'level': 'DEBUG',
         'handlers': ['console'],
         'propagate': False,
     }
    LOGGING['loggers']['celery'] = {
        'level': 'WARNING',
        'handlers': ['sentry'],
        'propagate': False,
    }
