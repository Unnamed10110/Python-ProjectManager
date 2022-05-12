'''El modelo para Proyecto, y relacion de usuarios con los mismos para que pueda identificarse, los atributos y metodos'''
from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import User
#from users.models import UserProfile
# Create your models here.
#from usuario.models import UserProfile
class Proyecto (models.Model):
    estados = (
        ('Pendiente','Pendiente'),
        ('Ejecutando', 'Ejecutando'),
        ('Cancelado', 'Cancelado'),
        ('Finalizado', 'Finalizado'),
    )
    nombre = models.CharField(max_length=50)
    fechaInicio=models.DateField()
    fechaFin = models.DateField()
    estado = models.CharField(max_length=50,choices=estados)
    scrum_master = models.CharField(max_length=50,default='')
    #usuarios = models.ManyToManyField(UserProfile)
    #users_stories
    #flujos
    #sprints
    def get_nombre(self):
        return self.nombre
    def get_fechaInicio(self):
        return self.fechaInicio
    def get_fechaFin(self):
        return self.fechaFin
    def get_estado(self):
        return self.estado
    def get_scrum(self):
        return self.scrum_master
    def get_usuarios(self):
        return self.usuarios

    def nombre_correcto(self, nombreNuevo):
        '''Verifica que no haya nombres de proyectos duplicados'''
        proyectos = Proyecto.objects.all()
        for p in proyectos:
            if nombreNuevo == p.nombre:
                return False
        return True
    def scrum_master_correcto(self, scrum):
        users = User.objects.all()
        for u in users:
            if scrum == u.username:
                return True
        return False
    def fechas_correctas(self, fecha1, fecha2):
        if fecha1 >= fecha2:
            return False
        return True

    def __iter__(self):
        return [
            self.nombre,
            self.scrum_master,
            self.fechaInicio,
            self.fechaFin,
            self.estado,
            self.usuarios
        ]

class Proyecto_User_Rol(models.Model):
    '''Modelo para relacionar proyectos, usuarios y roles'''
    usuario =  models.CharField(max_length=100,default='')
    proyecto = models.CharField(max_length=100,default='')
    rol = models.CharField(max_length=100,default='')


    def get_usuario(self):
        return self.usuario


    def get_proyecto(self):
        return self.proyecto


    def get_rol(self):
        return self.rol


    def __iter__(self):
        return [
            self.usuario,
            self.proyecto,
            self.rol
        ]
