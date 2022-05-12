
"""
Pruebas unitarias correspondientes a los Flujos.
    Pruebas realizadas:
        - Crear Flujo.
        - Crear Actividad
        - Modificar Flujo: Dentro de la Prueba Modificar Flujo se realizan las siguientes pruenas:
            - Asignar Actividades a Flujos
            - Modificar el Nombre del Flujo
            - Modificar una actividad del Flujo
            - Eliminar una actividad del Flujo
"""

from django.contrib.auth.models import User
from django.test import TestCase
import os
# Create your tests here.
from proyectos.models import Proyecto
from usuario.models import UserProfile
from tipoUS.models import tipo_us
from flujos.models import Flujos,Actividades
from userStory.models import UserStories
class FlujosModelsTest(TestCase):

            print('----------------------------------')
            print('Pruebas Unitarias para Flujos\n')
            print('----------------------------------')
            print ('En la base de datos auxiliar inicialmente existen:')
            print('Proyeto: Proy1')
            print ('Flujo: Flujo1')
            print('Actividad: Act1')
            print ('User: user1')
            print ('Tipo US: Infraestructura\n')

            def setUp(self):
                user=User.objects.create(username='user1',password='123')
                UserProfile.objects.create(user=user,direccion='alguna parte')
                proy=Proyecto.objects.create(nombre='Proy1',fechaInicio='2016-12-12',fechaFin='2016-12-15',scrum_master='user1')
                tpus=tipo_us.objects.create(nombre='Infraestructura')
                Flujos.objects.create(nombre='Flujo1',proyecto=proy,tipoUS=tpus)
                Actividades.objects.create(nombre='Act1',proyecto=proy)
                UserStories.objects.create(nombreUS='US1',id_proyecto=proy)
            def test_crear_actividad(self):

                print('\nPrueba: Crear una Actividad.')
                print('Nombre de la Actividad: Act2')
                print('Proyecto: Proy1')
                proy = Proyecto.objects.get(nombre='Proy1')
                act = Actividades.objects.create(nombre='Act2',proyecto=proy)
                msj = self.assertNotEquals(act,[])
                if msj == None:
                    print ('Se ha creado exitosamente la actividad: Act2 \n')
                os.system("pause")
                print('\n')

            def test_crear_flujo(self):

                print('\nPrueba: Crear un Flujo.')
                print('Nombre del Flujo: Flujo3')
                print('Proyecto: Proy1')
                print('Tipo US: Infraestructura')
                proy = Proyecto.objects.get(nombre='Proy1')
                tp = tipo_us.objects.get(nombre='Infraestructura')
                fl = Flujos.objects.create(nombre='Flujo3', proyecto=proy,tipoUS=tp)
                msj = self.assertEquals(fl.nombre, 'Flujo3')
                if msj == None:
                    print('\nSe ha creado exitosamente el Flujo: Flujo3 \n')
                os.system("pause")
                print('\n')

            def test_crear_ModificarFlujo(self):

                print('\nPrueba: Modificar un Flujo.')
                print('Nombre del Flujo: Flujo1')
                print('Proyecto: Proy1')
                print('Tipo US: Infraestructura\n')

                print('Modificacion a Realizar: Asignar la Actividad Act1\n')
                proy = Proyecto.objects.get(nombre='Proy1')
                fl = Flujos.objects.get(nombre='Flujo1')
                act = Actividades.objects.get(nombre='Act1')
                act.flujo = fl
                act.save()
                act = Actividades.objects.get(nombre='Act1')
                msj = self.assertEquals(act.flujo.nombre, 'Flujo1')
                if msj == None:
                    print('Se ha asignado exitosamente al Flujo: Flujo1 la actividad: Act1 \n')
                os.system("pause")
                print('\n')

                print('Modificacion a Realizar: Modificar nombre del Flujo1 a Flujo2\n')

                fl.nombre = 'Flujo2'
                fl.save()
                fl =Flujos.objects.get(nombre='Flujo2')
                msj = self.assertNotEquals(fl, [])
                if msj == None:
                    print('Se ha cambiado exitosamente el nombre del Flujo: de Flujo1 a Flujo2 \n')
                os.system("pause")
                print('\n')

                print('Modificacion a Realizar: Modificar la actividad Act1 del Flujo2,')
                print('Nuevo nombre: Act2.')

                act.nombre = 'Act2'
                act.save()
                act = Actividades.objects.get(nombre='Act2')
                msj = self.assertNotEquals(act, [])
                if msj == None:
                    print('Se ha modificado exitosamente la actividad: Act1 a Act2 en el Flujo2 \n')
                os.system("pause")
                print('\n')

                print('Modificacion a Realizar: Eliminar actividad Act2 del Flujo2\n')

                act.flujo = None
                act.save()
                act = Actividades.objects.get(nombre='Act2')
                msj = self.assertEquals(act.flujo, None)
                if msj == None:
                    print('Se ha eliminado exitosamente la actividad: Act2 del Flujo2 \n')
                os.system("pause")
                print('\n')

                print('Modificacion a Realizar: Asignar el US; US1 al Flujo: Flujo1\n')

                US=UserStories.objects.get(nombreUS='US1')
                US.actividad=act
                US.save()
                msj = self.assertEquals(US.actividad.nombre,act.nombre)
                if msj == None:
                    print('Se ha asignado el US: US1 al Flujo: Flujo1 \n')
                os.system("pause")
                print('\n')

