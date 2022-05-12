'''
configuracion del entorno de desarrollo del sistema, extendida de base.py
    - con base de datos de desarrollo separada
'''
from .base import *

DEBUG = True
ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'is2', # is2
        'USER': 'is2',
        'PASSWORD': '12345',#12345

    }
}
STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join('C:/GestorProyectos', 'static'),)

#STATICFILES_DIRS = (os.path.join('C:/Ester/GestorProyectos', 'static'),)

#MEDIA_ROOT = os.path.join('C:/Ester/GestorProyectos', 'media')
MEDIA_ROOT = os.path.join('C:/GestorProyectos', 'media')

MEDIA_URL = '/media/'