'''
configuracion del entorno de produccion del sistema, extendida de base.py
    - con base de datos de produccion separada
'''
from .base import *
DEBUG = True
ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'produccion', # is2
        'USER': 'is2',
        'PASSWORD': '12345',#12345

    }
}

STATIC_URL = '/static/'

STATICFILES_DIRS = (
	'static',
)
