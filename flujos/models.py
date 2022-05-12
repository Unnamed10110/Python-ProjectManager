
""""
Modelos necesarios para la creacion de Flujos.
Modelos:
    - Flujos
    - Actividades
"""

from django.db import models

from Sprints.models import Sprint
from usuario.models import UserProfile
from tipoUS.models import tipo_us
from proyectos.models import Proyecto



class Flujos(models.Model):
    """
    Clase Flujos:
    Atributos:
        - nombre: Nombre del Flujo
        - tipoUS: Tipo de User Story del Flujo
        - proyecto: Proyecto a que pertenece el flujo
    """
    nombre = models.CharField(max_length=100,default='')
    #actividades = models.ForeignKey(Actividades,default='',null=True)
    #miembros = models.ForeignKey(UserProfile,default='')
    tipoUS = models.ForeignKey(tipo_us,default='')
    proyecto = models.ForeignKey(Proyecto,default='')
    #users_stories = models.ManyToManyField(UserStories)
    sprint = models.ForeignKey(Sprint, null=True, default='')

    def controlarNombre(self,n):
        if Flujos.objects.filter(nombre=n):
            return False
        return True

    def controlarActividades(self,n):
        act = Actividades.objects.filter(nombre=n)
        nombre = Flujos.objects.filter(actividades=act.id)
        if nombre:
            return False
        return True

    def controlarMiembros(self, n):
        usr = UserProfile.objects.filter(nombre=n)
        nombre = Flujos.objects.filter(miembros=usr.id)
        if nombre:
            return False
        return True

    def controlarTipoUS(self,n):
        tipo = tipo_us.objects.filter(nombre=n)
        nombre = Flujos.objects.filter(tipoUS=tipo.id)
        if nombre:
            return False
        return True
    def obtenerPrimerActividad(self,idproyecto):
        proy = Proyecto.objects.get(pk=idproyecto)
        flujos = Flujos.objects.filter(proyecto=proy)
        for f in flujos:
            return f.actividad


class Actividades(models.Model):

    """
    Clase Actividades:
    Atributos:
        - nombre: nombre de la activiadad
        - proyecto: proyecto al que pertenece la activiadad
        - flujo: flujo al que pertenece la actividad
    """
    nombre = models.CharField(max_length=500,default='')
    #estado = models.ForeignKey(Estado,null=True)
    proyecto = models.ForeignKey(Proyecto,default='')
    flujo = models.ForeignKey(Flujos,default='',null=True)

    def controlarNombre(self,n):
        act = Actividades.objects.filter(nombre=n)
        if act:
            return False
        return True
