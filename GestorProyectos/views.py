'''
vista del modulo GestorProyectos
    - En esta vista se realizan las definiciones de permisos personalizados, las asignaciones de los permisos a los grupos(roles).
    - Tambien se definen los metodos de verificacion de acceso.
'''
from django.shortcuts import redirect, render, get_object_or_404
import os
from proyectos.models import Proyecto
from usuario.models import UserProfile
from django.contrib.auth.models import Permission , Group, User #,ContentType
from django.contrib.contenttypes.models import ContentType
from proyectos.models import Proyecto, Proyecto_User_Rol
from Sprints.models import Sprint
from flujos.models import Flujos
from tipoUS.models import tipo_us
from userStory.models import UserStories
from datetime import datetime


#--roles
administrador,a1=Group.objects.get_or_create(name='administrador')
scrum_master,sm1=Group.objects.get_or_create(name='scrum_master')
product_owner,po1=Group.objects.get_or_create(name='product_owner')
development_team,d1=Group.objects.get_or_create(name='development_team')
basico,b1=Group.objects.get_or_create(name='basico')

#--content types
ct_proyecto = ContentType.objects.get_for_model(Proyecto)
ct_usuario = ContentType.objects.get_for_model(UserProfile)
ct_sprint= ContentType.objects.get_for_model(Sprint)
ct_flujo= ContentType.objects.get_for_model(Flujos)
ct_us= ContentType.objects.get_for_model(UserStories)
ct_tipous= ContentType.objects.get_for_model(tipo_us)

#--permisos

permiso1,p1 = Permission.objects.get_or_create(codename='crear_proyecto', name='puede crear proyecto', content_type=ct_proyecto)
permiso2,p2 = Permission.objects.get_or_create(codename='crear_usuario', name='puede crear un usuario', content_type=ct_usuario)
permiso3,p3 = Permission.objects.get_or_create(codename='eliminar_usuario', name='puede eliminar un usuario', content_type=ct_usuario)
#permiso4,p4 = Permission.objects.get_or_create(codename='eliminar_proyecto', name='puede eliminar un proyecto', content_type=ct_proyecto)
permiso5,p5 = Permission.objects.get_or_create(codename='modificar_proyecto', name='puede modificar un proyecto', content_type=ct_proyecto)
permiso6,p6 = Permission.objects.get_or_create(codename='crear_flujo', name='puede crear/importar un flujo', content_type=ct_flujo)
permiso7,p7 = Permission.objects.get_or_create(codename='modificar_flujo', name='puede modificar un flujo', content_type=ct_flujo)
permiso8,p8 = Permission.objects.get_or_create(codename='crear_us', name='puede crear un user story', content_type=ct_us)
permiso9,p9 = Permission.objects.get_or_create(codename='modificar_us', name='puede modificar un user story', content_type=ct_us)
permiso10,p10 = Permission.objects.get_or_create(codename='crear_sprint', name='puede crear un sprint', content_type=ct_sprint)
permiso11,p11 = Permission.objects.get_or_create(codename='modificar_sprint', name='puede modificar un sprint', content_type=ct_sprint)
permiso12,p12 = Permission.objects.get_or_create(codename='asignar_usuario', name='puede asignar usuarios al proyecto', content_type=ct_proyecto)
permiso13,p13 = Permission.objects.get_or_create(codename='asignar_us_sprint', name='puede asignar us al sprint', content_type=ct_sprint)
permiso0,p0 = Permission.objects.get_or_create(codename='acceso_basico', name='puede visualizar componentes basicos', content_type=ct_proyecto)
permiso,p = Permission.objects.get_or_create(codename='admin', name='es administrador', content_type=ct_proyecto)
permiso14,p14= Permission.objects.get_or_create(codename='ver_backlog', name='puede ver backlog',content_type=ct_sprint)

#--asignaciones de permisos a roles


administrador.permissions.add(permiso1,permiso2,permiso3,permiso0,permiso)
scrum_master.permissions.add(permiso5,permiso6,permiso7,permiso8,permiso9,permiso10,permiso11,permiso12,permiso13,permiso0)
product_owner.permissions.add(permiso5,permiso0)
development_team.permissions.add(permiso0,permiso14)
basico.permissions.add(permiso0)

def micuenta(request):
    '''verificacion de autenticacion del usuario'''
    if not request.user.is_authenticated():
        return redirect('login')
    else:
        usuario2 = UserProfile.objects.get(user__username=request.user)
    return render(request, "MiCuenta.html", {'usuario': usuario2})


def administracion(request):
    '''acceso al modulo de administracion del sistema'''
    return render(request, 'administracion.html', {})



def ver_proyecto(request, proyectoid):
    '''visualizacion y acceso al proyecto de un usuario con sus respectivos permisos'''
    #usuariop=request.user
    usuariop=User.objects.get(username=request.user)
    usuariop.user_permissions.clear()
    print (usuariop.get_all_permissions(), "\n---------permisos de usuario son 0")

    usuariop.groups.clear()

    upr = Proyecto_User_Rol.objects.get(usuario=usuariop.username, proyecto=Proyecto.objects.get(id=proyectoid).nombre)
    print ("-----",upr.rol,"-------")
    if upr.rol=='development':
        print ("es desarrollador---------")
        #development_team.permissions.clear()
        #usuariop.user_permissions.clear()
        usuariop.groups.add(development_team)
    if upr.rol == 'product_owner':
        print ("es product owner")
        development_team.permissions.clear()
        usuariop.groups.add(product_owner)
    if upr.rol == 'scrum_master':

        #development_team.permissions.clear()
        usuariop.groups.add(scrum_master)


    print (usuariop.get_all_permissions(),"---------permisos de usuario")
    #permiso=usuariop.has_perm(u'auth.add_prueba2')
    proyecto = get_object_or_404(Proyecto, pk=proyectoid)
    lista_nombres = Proyecto_User_Rol.objects.filter()

    return render(request, 'ver_proyecto.html', {'proyectoid': proyectoid, 'proyecto':proyecto,'lista_nombres': lista_nombres,})

def log(logn,*param):
    '''Metodo para generar registros de actividades. Recibe n parametros.'''
    c=0
    fecha = datetime.now()
    fecha = fecha.strftime('%A/%Y/%m/%d %H:%M:%S')
    b='F:/'
    logn=b+logn
    with open(logn, 'a') as file:
        file.write('# ')
        for var in param:
            #if not param: break
            #var=param
            if c==0: file.write('[objeto: %s]\t-' % var)
            if c == 1: file.write('[operacion: %s]\t-' % var)
            if c == 2: file.write('[sujeto: %s]\t-' % var)
            if c > 2 : file.write(' "%s"\t-' % var)
            c = c + 1
        file.write('[%s]\t\n' % fecha)
