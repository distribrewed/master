import os

import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '$+^g53vd0(m-by2&1joz1vh+d)42q&suqbkv@c62)z+auel@0b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DISTRIBREWED_USER = os.environ.get('DISTRIBREWED_USER', 'admin')
DISTRIBREWED_PASS = os.environ.get('DISTRIBREWED_PASS', 'admin')

# Application definition
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
]

ADMIN_APPS = [
    'admin_interface',
    'flat_responsive',
    'colorfield',
    #'django-admin-bootstrapped.bootstrap3',
    #'django-admin-bootstrapped',
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_docs',
]

USER_APPS = [
    'masters',
    'workers',
    'brew',
    'grafana',
]

INSTALLED_APPS = DJANGO_APPS + ADMIN_APPS + THIRD_PARTY_APPS + USER_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    )
}

ROOT_URLCONF = 'distribrewed.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'distribrewed', 'templates')],
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

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

WSGI_APPLICATION = 'distribrewed.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'NAME': os.environ.get('DB_NAME', 'distribrewed'),
        'USER': os.environ.get('DB_USER', 'distribrewed'),
        'PASSWORD': os.environ.get('DB_PASS', 'secretpass'),
    }
}

CONSUL = {
    'host': os.environ.get('CONSUL_SERVER_HOST', 'localhost'),
    'port': int(os.environ.get('CONSUL_SERVER_PORT', '8500')),
}

PROMETHEUS = {
    'host': os.environ.get('PROMETHEUS_SERVER_HOST', 'localhost'),
    'port': int(os.environ.get('PROMETHEUS_SERVER_PORT', '9090')),
}

GRAFANA = {
    'host': os.environ.get('GRAFANA_SERVER_HOST', 'localhost'),
    'port': int(os.environ.get('GRAFANA_SERVER_PORT', '3000')),
    'user': os.environ.get('GRAFANA_SERVER_USER', DISTRIBREWED_USER),
    'pass': os.environ.get('GRAFANA_SERVER_PASS', DISTRIBREWED_PASS),
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

# Logging
DEBUG_PROPAGATE_EXCEPTIONS = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(pathname)s:%(lineno)s: [%(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'distribrewed': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'masters': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'workers': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
}
