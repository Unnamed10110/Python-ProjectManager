'''
modelo del modulo tipoUS
    -se definen los campos de la Tipo User Story
'''
from django.db import models

# Create your models here.
class tipo_us(models.Model):
    '''clase con los atributos del modelo tipoUS- Incluyendo Get's y Set's'''
    nombre = models.CharField(max_length=50)
    descripcion= models.CharField(max_length=500)

    def nombre_doble(self, nombre):
        tipoUS = tipo_us.objects.all()
        for tus in tipoUS:
            if tus.nombre == nombre:
                return False
        return True

    def get_nombre(self):
        return self.nombre

    def __iter__(self):
        return [
            self.nombre,
        ]
