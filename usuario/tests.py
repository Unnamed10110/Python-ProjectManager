import os
from django.test import TestCase
from django.contrib.auth.models import User
from usuario.models import UserProfile
from proyectos.models import Proyecto_User_Rol
# Create your tests here.
class UsuarioTestCase(TestCase):
    print('----------------------------------')
    print('Pruebas Unitarias para Usuarios\n')
    print('----------------------------------')
    print ('En la base de datos auxiliar inicialmente exiten:')
    print ('User: user1.\n')

    def setUp(self):
        user = User.objects.create(username='user1', password='123')
        UserProfile.objects.create(user=user, direccion='alguna parte')

    def test_crear_usuario(self):
        print('\nPrueba de Creacion de un Usuario.')
        print('username: user2')
        print('Nombre: user2')
        print('password : 123')

        user = User.objects.create(username='user2', password='123')
        usuario = UserProfile.objects.create(user=user, direccion='alguna parte')

        msj = self.assertNotEqual(usuario,[])
        if msj == None:
            print ('\nUsuario '+usuario.user.username+' creado exitosamente.\n')
        os.system("pause")
    def test_crear_usuario_duplicado(self):

        print('\nPrueba de Creacion de un Usuario cuyo nombre ya existe en la BD.')
        print('username: user2')
        print('Nombre: user2')
        print('password : 123')

        user = UserProfile()
        msj = self.assertNotEqual(user.nombre_valido('user2'), False)
        if msj == None:
            print ('\nuser2 no creado, ya existe en la BD.\n')
        os.system("pause")
    def test_modificar_usuario(self):
        print('\nPrueba de Modificacion de un Usuario. Se probara con el usuario:')
        print('username: user1')
        print('Nombre: user1')
        print('password : 123')

        print('Nuevos datos: ')
        print('Nombre: alguien')

        user = User.objects.get(username='user1')
        user.first_name = 'alguien'
        user.save()
        user = User.objects.get(username='user1')
        msj = self.assertEquals(user.first_name,'alguien')
        if not msj:
            print('\nSe ha guardado correctamente las modificaciones')
        else:
            print('No se ha podido guardar las modificaciones')
        os.system("pause")
    def test_cambiar_contrasenha(self):
        print('\nPrueba de cambiar contranhera a un usuario.')
        print('username: user1')
        print('Nombre: user1')
        print('password original: 123')
        print('password nuevo: 456')
        user = User.objects.get(username='user1')
        user.set_password('456')
        user.save()

        user = User.objects.get(username='user1')
        msj = self.assertEqual(user.check_password('456'),True)
        if msj == None:
           print('\nSe ha cambiado la contrasenha a: 456')
        else:
           print('NO ha cambiado la contrasenha a: 456')
        os.system("pause")
    def test_elimnar_usuario(self):

        print('\nPrueba de Eliminar usuario.\nUsuario de prueba:')
        print('username: user1')
        user = UserProfile.objects.get(user__username='user1')
        print('verificamos que no tenga ningun rol asociado a algun proyecto\n')
        roles = Proyecto_User_Rol.objects.all()
        msj = self.assertNotEquals(roles.filter(usuario='user1'),[])
        if msj == None:
            print ('\nEl usuario user1 puede ser eliminado del proyecto.')
            user.user.delete()
            user.delete()
            msj2 = self.assertNotEquals(User.objects.filter(username='user1'),['<User : Object >'])
            if msj2 == None:
                print('Usuario user1 elimnado correctamente')
        else:
            print('\nEste usuario tienen un rol en un proyecto\nNo puede eliminarse')
        os.system("pause")