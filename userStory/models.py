'''Se presenta el modelo de US para el sistema, las restricciones
que se deben tener en cuenta en cuanto a su asignacion a usuarios,
creacion y modificacion'''

from __future__ import unicode_literals
from django.db import models
from Sprints.models import Sprint
from flujos.models import Actividades
from proyectos.models import Proyecto
from tipoUS.models import tipo_us
from usuario.models import UserProfile
from datetime import datetime

class UserStories(models.Model):
    '''
    :param la extension de la clase models
    Todos los atributos que son necesarios para que un US sea identificado'''
    id_proyecto=models.ForeignKey(Proyecto,null=True)
    sprint = models.ForeignKey(Sprint, null=True)
    tipoUS = models.ForeignKey(tipo_us,null=True)
    usuario_asignado = models.ForeignKey(UserProfile, null=True)
    nombreUS=models.CharField(max_length=50,default='')
    valor_negocio = models.FloatField(default=0)
    valor_tecnico = models.FloatField(default=0)
    prioridad_cliente = models.FloatField(default=0)
    prioridad = models.FloatField(default=0)
    tiempo_planificado=models.FloatField(default=0)
    tiempo_ejecutado=models.FloatField(default=0)
    tiempo_acumulado=models.FloatField(default=0)
    descripcion_corta=models.CharField(max_length=80,default='')
    descripcion_larga=models.TextField(max_length=5000,default='')
    notas = models.TextField(max_length=6000, default='')
    terminado=models.BooleanField(default=False)
    estado = models.CharField(max_length=100, default='', null=True)
    actividad = models.ForeignKey(Actividades, default='', null=True)

    # criterio_de_aceptacion=models.
    def nombre_duplicado(self,nombre,proyectoid):
        '''Comprueba que no existan US con el mismo nombre'''
        ustory = UserStories.objects.filter(id_proyecto=Proyecto.objects.get(pk=proyectoid))
        for us in ustory:
            if us.nombreUS == nombre:
                return False
        return True

    def asignado_a_user(self,usuario):
        '''Evalua que ningun usuario pueda tener sobrecarga de trabajo'''
        if usuario.captrabajo<=usuario.trabasignado:
            return False
        return True
'''
class archivos(models.Model):
    #filename = models.CharField(max_length=100, null=True)
    archivos_adjuntos = models.FileField(upload_to='adjuntos', null=True)
    us=models.ForeignKey(UserStories)
'''
