#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


from django.db import models
from django.conf import settings
from  django.contrib.auth.models import User
from proyectos.models import Proyecto

class UserProfile(models.Model):
    '''Se definen todos los atributos para que un Usuario sea identificado dentro de un sistema.'''
    user = models.OneToOneField(User)
    direccion = models.CharField(max_length=50, default='')
    telefono = models.CharField(max_length=50, default='')
    captrabajo = models.IntegerField(default=0)
    trabasignado = models.FloatField(default=0)
    descripcion = models.CharField(max_length=240, default='')
    es_administrador = models.BooleanField(default=False)
    proyectos = models.ManyToManyField(Proyecto,default=None)

    def nombre_valido(self,nombre):
        '''verifica que el usuario no exista en la BD'''
        users = UserProfile.objects.all()
        for u in users:
            if u.user.username == nombre:
                return False
        return True
