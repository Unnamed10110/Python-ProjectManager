from django.contrib.auth.models import User
from django.test import TestCase
import os
# Create your tests here.
from proyectos.models import Proyecto
from userStory.models import UserStories
from usuario.models import UserProfile
from tipoUS.models import tipo_us
from flujos.models import Flujos,Actividades
from Sprints.models import Sprint,Sprint_Usuarios

class FlujosModelsTest(TestCase):

            print('----------------------------------')
            print('Pruebas Unitarias para Sprints\n')
            print('----------------------------------')
            print ('En la base de datos auxiliar inicialmente existen:')
            print('Proyeto: Proy1')
            print ('User: user1')
            print('User Story: US1')
            print('Sprint: Sprint1')
            print('Flujo: Flujo1')

            def setUp(self):
                user=User.objects.create(username='user1',password='123')
                UserProfile.objects.create(user=user,direccion='alguna parte')
                proy=Proyecto.objects.create(nombre='Proy1',fechaInicio='2016-12-12',fechaFin='2016-12-15',scrum_master='user1')
                tpus=tipo_us.objects.create(nombre='Infraestructura')
                UserStories.objects.create(nombreUS='US1', id_proyecto=proy, tipoUS=tpus)
                Sprint.objects.create(nombre='Sprint1',id_proyecto=proy ,fechaInicio='2016-12-16',tiempo_asignado=0,duracion=2)
                Flujos.objects.create(nombre='Flujo1',proyecto=proy,tipoUS=tpus)

            def test_crear_Sprint(self):

                print('\nPrueba: Crear un Sprint.')
                print('Nombre del Sprint: Sprint2')
                print ('Fecha Inicio: 2016/12/19')
                print('Proyecto: Proy1')
                proy = Proyecto.objects.get(nombre='Proy1')
                sp = Sprint.objects.create(nombre='Sprint2',id_proyecto=proy,fechaInicio='2016-12-19',tiempo_asignado=0,duracion=2)
                msj = self.assertNotEquals(sp,[])
                if msj == None:
                    print ('Se ha creado exitosamente el Sprint: Sprint2 \n')
                os.system("pause")
                print('\n')

            def test_Modificar_Sprint(self):

                print('\nPrueba: Modificar un Sprint.')
                print('Nombre del Sprint: Sprint1')
                print('User Story: US1')

                print ('\nModicacion a realizar: Asignar US al Sprint')
                us = UserStories.objects.get(nombreUS='US1')
                sp = Sprint.objects.get(nombre='Sprint1')
                us.sprint=sp
                us.save()
                us = UserStories.objects.get(nombreUS='US1')
                msj = self.assertEquals(us.sprint.nombre, 'Sprint1')
                if msj == None:
                    print('\nSe ha asignado exitosamente el US: US1 al Sprint: Sprint1 \n')
                os.system("pause")
                print('\n')

                print('\nModicacion a realizar: Asignar Usuario al Sprint')
                usr = User.objects.get(username='user1')
                usr = UserProfile.objects.get(user=usr)
                sp = Sprint.objects.get(nombre='Sprint1')
                spu=Sprint_Usuarios.objects.create(usuario=usr.user.username,sprint=sp.nombre)
                msj = self.assertEquals(spu.usuario, 'user1')
                if msj == None:
                    print('\nSe ha asignado exitosamente el Usuario: user1 al Sprint: Sprint1 \n')
                os.system("pause")
                print('\n')

                print('\nModicacion a realizar: Asignar Flujo al Sprint')
                flujo = Flujos.objects.get(nombre='Flujo1')
                sp = Sprint.objects.get(nombre='Sprint1')
                flujo.sprint = sp
                flujo.save()
                msj = self.assertEquals(flujo.sprint.nombre, 'Sprint1')
                if msj == None:
                    print('\nSe ha asignado exitosamente el Flujo: Flujo1 al Sprint: Sprint1 \n')
                os.system("pause")
                print('\n')

