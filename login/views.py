'''En esta porcion de codigo se realizan las comprobaciones para cada sesion del usuario, entrar
al sistema, salir del sistema e ingresar a la Pagina principal '''
from django.shortcuts import redirect
from login.forms import loginform
from django.template import RequestContext
from django.shortcuts import render_to_response
from login.forms import loginform
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import Permission , Group, User #,ContentType
from django.contrib.contenttypes.models import ContentType

administrador,a1=Group.objects.get_or_create(name='administrador')

#------------------------permisos

from django.contrib.auth.models import Permission , Group #,ContentType
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
#--------modelos de las aplicaciones
from proyectos.models import Proyecto
from usuario.models import UserProfile

#print "------------------prueba permisos\n"
'''
#--roles
administrador,a1=Group.objects.get_or_create(name='administrador')
scrum_master,sm1=Group.objects.get_or_create(name='scrum_master')
product_owner,po1=Group.objects.get_or_create(name='product_owner')
development_team,d1=Group.objects.get_or_create(name='development_team')
basico,b1=Group.objects.get_or_create(name='basico')

#--content types
ct_proyecto = ContentType.objects.get_for_model(Proyecto)
ct_usuario = ContentType.objects.get_for_model(UserProfile)

#--permisos

permiso1,p1 = Permission.objects.get_or_create(codename='crear_proyecto', name='puede crear proyecto', content_type=ct_proyecto)
permiso2,p2 = Permission.objects.get_or_create(codename='crear_usuario', name='puede crear un usuario', content_type=ct_usuario)
permiso3,p3 = Permission.objects.get_or_create(codename='eliminar_usuario', name='puede eliminar un usuario', content_type=ct_usuario)
#permiso4,p4 = Permission.objects.get_or_create(codename='eliminar_proyecto', name='puede eliminar un proyecto', content_type=ct_proyecto)
permiso5,p5 = Permission.objects.get_or_create(codename='modificar_proyecto', name='puede modificar un proyecto', content_type=ct_proyecto)
#permiso6,p6 = Permission.objects.get_or_create(codename='crear_flujo', name='puede crear/importar un flujo', content_type=ct_flujo)
#permiso7,p7 = Permission.objects.get_or_create(codename='modificar_flujo', name='puede modificar un flujo', content_type=ct_flujo)
#permiso7,p7 = Permission.objects.get_or_create(codename='crear_us', name='puede crear un user story', content_type=ct_us)
#permiso7,p7 = Permission.objects.get_or_create(codename='modificar_us', name='puede modificar un user story', content_type=ct_us)
#permiso8,p8 = Permission.objects.get_or_create(codename='crear_sprint', name='puede crear un sprint', content_type=ct_sprint)
#permiso9,p9 = Permission.objects.get_or_create(codename='modificar_sprint', name='puede modificar un sprint', content_type=ct_sprint)
permiso6,p6 = Permission.objects.get_or_create(codename='asignar_usuario', name='puede asignar usuarios al proyecto', content_type=ct_proyecto)
#permiso7,p7 = Permission.objects.get_or_create(codename='asignar_us_sprint', name='puede asignar us al sprint', content_type=ct_sprint)
permiso0,p0 = Permission.objects.get_or_create(codename='acceso_basico', name='puede visualizar componentes basicos', content_type=ct_proyecto)


#--asignaciones de permisos a roles

administrador.permissions.add(permiso1,permiso2,permiso3,permiso0)
scrum_master.permissions.add(permiso5,permiso6,permiso0)
product_owner.permissions.add(permiso5,permiso0)
development_team.permissions.add(permiso0)
basico.permissions.add(permiso0)


#------ caja booleana

#os.system("pause")

'''

ct_proyecto = ContentType.objects.get_for_model(Proyecto)
permiso,p = Permission.objects.get_or_create(codename='admin', name='es administrador', content_type=ct_proyecto)
def login_page(request):
    """
        :param Recibe una solicitud de conexion con el servidor
        :return login.html
        Redirige a la pag de Logueo donde se comprueba si el usuario ingreso sus datos correctamente,
        si esta activo en el sistema, y si sus datos se encuentran en la base de datos
    """
    message=None
    if request.method == "POST":
      form=loginform(request.POST)
      if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
        #    print username
       #     print password
            if user is not None:
                if user.is_active:
                    login(request,user)
                    print(user.id)
                    up=UserProfile.objects.get(user_id=user.id)
                    if up.es_administrador == True:
                        user.user_permissions = [permiso]

                    return redirect('homepage')
                    #return redirect('crearproyecto')
                    #return redirect('crearusuario')
                else:
                    message="Usuario inactivo"
            else:
                message="Datos incorrectos"
    else:
        form=loginform()
    return render_to_response('login.html',  {'message':message,'form': form}, context_instance=RequestContext(request))

def homepage(request):
    """
        :param Recibe una solicitud de conexion con el servidor
        :return PagPricipal.html
        Si el usuario fue logueado correctamente, se lo redirige a la pagina principal del Sistema,
        con los permisos correspondientes de tal usuario
    """
    up = User.objects.get(username=request.user)
    user=UserProfile.objects.get(user=up)
    if user.es_administrador == True:
        up.user_permissions = [permiso]
    return render_to_response('index.html', context_instance=RequestContext(request))

def salir(request):
    """
        :param Recibe una solicitud de conexion con el servidor
        :return redireccion a la vista login
        Cierra la sesion del usuario, y lo redirige a la pag de login
    """
    logout(request)
    return redirect('login')

'''---------- bases ----------
import os
from django.contrib.auth.models import Permission , Group #,ContentType
from django.contrib.contenttypes.models import ContentType
from myapp.models import clase
ct_proyecto = ContentType.objects.get_for_model(Proyecto)
permiso1,p1 = Permission.objects.get_or_create(codename='crear_proyecto', name='puede crear proyecto', content_type=ct_proyecto)
administrador,a1=Group.objects.get_or_create(name='administrador')
administrador.permissions.add(permiso1)
user = User.objects.get(username='duke_nukem')
group = Group.objects.get(name='wizard')
group.permissions.add(permission)
user.groups.add(group)
print user.get_all_permissions()
user.user_permissions = [permiso1,permiso2,permiso3,permiso4]
u.groups.add(g_prueba1)
print u.has_perm(u'auth.add_prueba2')

{% if perms.miapp.permiso_personalizado %}
			<p>listo</p>
{% endif %}
'''