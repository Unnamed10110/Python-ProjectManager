from django.contrib.auth.models import User
from django.test import TestCase
import os
# Create your tests here.
from proyectos.models import Proyecto
from usuario.models import UserProfile
from tipoUS.models import tipo_us
from flujos.models import Flujos,Actividades
from userStory.models import UserStories

class userStoryModelsTest(TestCase):

            print('----------------------------------')
            print('Pruebas Unitarias para User Stories\n')
            print('----------------------------------')
            print ('En la base de datos auxiliar inicialmente existen:')
            print('Proyeto: Proy1')
            print ('User: user1')
            print ('Tipo US: Infraestructura')
            print ('User Story: US1\n')

            def setUp(self):
                user=User.objects.create(username='user1',password='123')
                UserProfile.objects.create(user=user,direccion='alguna parte')
                proy=Proyecto.objects.create(nombre='Proy1',fechaInicio='2016-12-12',fechaFin='2016-12-15',scrum_master='user1')
                tpus=tipo_us.objects.create(nombre='Infraestructura')
                UserStories.objects.create(nombreUS='US1',id_proyecto=proy,tipoUS=tpus)

            def test_us(self):

                print('\nPrueba: Crear un User Story.')
                print ('Nombre: US2 ')
                print('Proyecto: Proy1')
                print ('Tipo de US: Infraestructura')
                proy = Proyecto.objects.get(nombre='Proy1')
                tp = tipo_us.objects.get(nombre='Infraestructura')
                act = UserStories.objects.create(nombreUS='US2',id_proyecto=proy,tipoUS=tp)
                msj = self.assertNotEquals(act,[])
                if msj == None:
                    print ('Se ha creado exitosamente el User Story: US2 \n')
                os.system("pause")
                print('\n')

            def test_ModificarUS(self):

                print('\nPrueba: Modificar un User Story.')
                print('Nombre del US: US1')
                print('Proyecto: Proy1')
                print('Tipo US: Infraestructura')
                print ('Usuario: user1\n')

                print('Modificacion a Realizar: Asignar el usuario user1\n')
                proy = Proyecto.objects.get(nombre='Proy1')
                usr = User.objects.get(username='user1')
                usr = UserProfile.objects.get(user=usr)
                us = UserStories.objects.get(nombreUS='US1')
                us.usuario_asignado  = usr
                us.save()
                us = UserStories.objects.get(nombreUS='US1')
                msj = self.assertEquals(us.usuario_asignado.user.username, 'user1')
                if msj == None:
                    print('Se ha asignado exitosamente al US: US1 el usuario: user1 \n')
                os.system("pause")
                print('\n')
