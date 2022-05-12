import os
from django.test import TestCase
from django.test.client import Client
from proyectos.models import Proyecto,Proyecto_User_Rol
from usuario.models import UserProfile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# Create your tests here.

class ProyectosViewsTest(TestCase):

            print('----------------------------------')
            print('Pruebas Unitarias para Proyectos\n')
            print('----------------------------------')
            print ('En la base de datos auxiliar inicialmente existen:')
            print ('Proyecto: proy1')
            print ('User: fer\n')

            def setUp(self):
                user=User.objects.create(username='fer',password='123')
                UserProfile.objects.create(user=user,direccion='alguna parte')
                Proyecto.objects.create(nombre='proy1',fechaInicio='2016-12-12',fechaFin='2016-12-15',scrum_master='fer')


            def test_crear_proyecto(self):

                print('\nPrueba de Creacion de un Proyecto.')
                print('Nombre del proyecto: proy2')
                print('FechaInicio : 2016-12-12')
                print('FechaFin : 2016-12-15')
                print('Scrum Master : fer\n')

                proyecto = Proyecto.objects.create(nombre='proy2',fechaInicio='2016-12-12',fechaFin='2016-12-15',scrum_master='fer')
                msj = self.assertNotEqual(proyecto,[])
                if msj == None:
                    print ('Se ha creado exitosamente el proyecto: proy1 \n')
                os.system("pause")
            def test_crear_proyecto_duplicado(self):
                print('\nPrueba de Creacion de un Proyecto Duplicado.')
                print('Nombre del nuevo proyecto: proy1')
                print('FechaInicio : 2016-12-12')
                print('FechaFin : 2016-12-15')
                print('Scrum Master : fer')
                proyectos = Proyecto()

                msj = self.assertEqual(proyectos.nombre_correcto('proy1'),False)
                if msj == None:
                    print ('\nSe ha evitado crear un proyecto con el mismo nombre a uno existente.\n')
                os.system("pause")
            def test_crear_proyecto_fecha(self):
                print('\nSe debe evitar crear un proyecto con una fecha invalida.')
                print('Nombre del nuevo proyecto: proy3')
                print('FechaInicio : 2016-12-12')
                print('FechaFin : 2016-12-12')
                print('Scrum Master : fer')
                proyectos = Proyecto()

                msj = self.assertEqual(proyectos.fechas_correctas('2016-12-12','2016-12-12'), False)
                if msj == None:
                    print ('\nSe ha evitado crear un proyecto con una fecha invalida.\n')
                os.system("pause")
            def test_crear_proyecto_scrum(self):
                print('\nSe debe evitar asignar a un proyecto como scrum master un usuario inexistente.')
                print('Nombre del nuevo proyecto: proy4')
                print('FechaInicio : 2016-12-12')
                print('FechaFin : 2016-12-12')
                print('Scrum Master : alguien')
                proyectos = Proyecto()

                msj = self.assertEqual(proyectos.scrum_master_correcto('alguien'), False)
                if msj == None:
                    print ('\nNo se ha asignado al proyecto un Scrum master Inexistente.\n')
                os.system("pause")
            def test_asignar_usuario_proyecto(self):
                print('\nPrueba Asignar un usuario a un proyecto.\nUsuario de prueba:')
                print('username: fer')
                print('rol : Scrum Master')
                print('Proyecto de prueba: ')
                print('nombre: proy1')

                proy = Proyecto.objects.get(nombre='proy1')
                user  = UserProfile.objects.get(user__username='fer')

                Proyecto_User_Rol.objects.create(usuario='user1',proyecto='proy1',rol='Scrum Master')

                msj = self.assertNotEqual(Proyecto_User_Rol.objects.get(usuario='user1'),[])
                if not msj:
                    print('\nSe ha agregado el usuario user1 al proyecto\n')
                else:
                    print('\nNo se ha agregado el usuario user1 al proyecto\n')
                os.system("pause")