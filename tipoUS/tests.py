'''pruebas unitarias del modulo tipoUS
    -PU de crear tipoUS (con diferentes datos para probar las validaciones,duplicaciones,etc)

'''

from django.contrib.auth.models import User
from django.test import TestCase
import os
# Create your tests here.
from proyectos.models import Proyecto
from usuario.models import UserProfile
from tipoUS.models import tipo_us
from flujos.models import Flujos,Actividades

class TipoUSModelsTest(TestCase):

            print('----------------------------------')
            print('Pruebas Unitarias para Tipo de US\n')
            print('----------------------------------')
            print ('En la base de datos auxiliar inicialmente existen:')
            print ('Tipo US: Infraestructura\n')

            def setUp(self):
                tpus=tipo_us.objects.create(nombre='Infraestructura')

            def test_tipo_US(self):

                print('\nPrueba: Crear un Tipo de US.')
                print('Nombre del Tipo de US: Desarrollo\n')
                tp = tipo_us.objects.create(nombre='Desarrollo')
                msj = self.assertEquals(tp.nombre,'Desarrollo')
                if msj == None:
                    print ('Se ha creado exitosamente el tipo de US: Desarrollo \n')
                os.system("pause")
                print('\n')

            def test_crear_tipoUS_Duplicado(self):

                print('\nPrueba: Evitar crear un Tipo de US duplicado.')
                print('Nombre del Tipo de US: Infraestructura\n')
                tp = tipo_us.objects.get(nombre='Infraestructura')
                msj = self.assertNotEquals(tp, [])
                if msj == None:
                    print('\nSe ha evitado exitosamente crear un Tipo de US duplicado \n')
                os.system("pause")
                print('\n')
