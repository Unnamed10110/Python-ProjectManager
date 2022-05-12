import os, sys

sys.path.append('C:/Apache24/htdocs/GestorProyectos')

os.environ['DJANGO_SETTINGS_MODULE'] = 'GestorProyectos.settings.development'

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
