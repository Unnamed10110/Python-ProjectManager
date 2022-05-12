''' Modelo de Sprint para que pueda ser identificado, que contiene todos los atributos y los metodos
para que sea funcional '''
from django.db import models
from proyectos.models import Proyecto

class Sprint(models.Model):
    '''Todos los atributos para que un Sprint sea identificado'''
    nombre=models.CharField(max_length=50, default='')
    duracion=models.IntegerField()
    fechaInicio = models.DateField(null=True)
    fechaFin =models.DateField(null=True)
    id_proyecto=models.ForeignKey(Proyecto, null=True)
    tiempo_asignado=models.FloatField(default=0,null=True)
    estados = (
        ('Pendiente', 'Pendiente'),
        ('Ejecutando', 'Ejecutando'),
        ('Cancelado', 'Cancelado'),
        ('Finalizado', 'Finalizado'),
    )
    estado = models.CharField(max_length=50, choices=estados)
    def get_nombre(self):
        return self.nombre

    def get_fechaInicio(self):
        return self.fechaInicio

    def get_fechaFin(self):
        return self.fechaFin

    def get_estado(self):
        return self.estado
    def nombre_correcto(self, nombreNuevo):
        sprints = Sprint.objects.all()
        for p in sprints:
            if nombreNuevo == p.nombre:
                return False
        return True

    def __iter__(self):
        return [
            self.nombre,
            self.fechaInicio,
            self.estado,
        ]

class Sprint_Usuarios(models.Model):
    '''Relacion existente entre miembros de un Sprint'''
    usuario=models.CharField(max_length=50,default='')
    sprint=models.CharField(max_length=50,default='')

    def __iter__(self):
        return [
            self.usuario,
            self.sprint,
        ]
