'''Se permite la creacion de usuarios, la modificacion de datos de la cuenta
actual que adquiere en el sistema'''
from django.contrib.auth.models import Permission , Group #,ContentType
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from proyectos.models import Proyecto, Proyecto_User_Rol
from django.contrib.auth.models import User
from django.shortcuts import render
from usuario.models import UserProfile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, send_mass_mail

ct_proyecto = ContentType.objects.get_for_model(Proyecto)
'''
administrador,a1=Group.objects.get_or_create(name='administrador')
scrum_master,sm1=Group.objects.get_or_create(name='scrum_master')
product_owner,po1=Group.objects.get_or_create(name='product_owner')
development_team,d1=Group.objects.get_or_create(name='development_team')
basico,b1=Group.objects.get_or_create(name='basico')

#--content types

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



scrum_master.permissions.add(permiso5,permiso6,permiso7,permiso8,permiso9,permiso10,permiso11,permiso12,permiso13,permiso0)
product_owner.permissions.add(permiso5,permiso0)
development_team.permissions.add(permiso0,permiso14)
basico.permissions.add(permiso0)
'''

permiso,p = Permission.objects.get_or_create(codename='admin', name='es administrador', content_type=ct_proyecto)
def registrousuario(request):
    '''Permite la  creacion de una cuenta de  usuario en el sistema, teniendo en cuenta sus datos personales
    y una contrasenha para su autentificacion dentro del mismo. Controla que no existan username duplicados '''
    mensaje=None
    flag=0
    if request.method == "POST":
        #verificamos que el usuario no exista en la BD
        username = request.POST['username']
        if User.objects.filter(username=username):
            mensaje="Ya existe un usuario con este username"
            flag=1
        email=request.POST['email']
        if not ValidateEmail(email):
            flag=1
            if not mensaje:
                mensaje= "El mail ingresado no es correcto"
            else:
                mensaje += " - El mail ingresado no es correcto"
        if User.objects.filter(email=email):
            flag = 1
            if not mensaje:
                mensaje = "El mail ingresado ya ha sido registrado"
            else:
                mensaje += " - El mail ingresado ya ha sido registrado"
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            if not mensaje:
                mensaje = "Las contrasenhas no coinciden"
            else:
                mensaje += " - Las contrasenhas no coinciden"
            flag=1
        if not flag:
            send_mail(
                'Nuevo en SGP',
                'Han creado una cuenta para ti en SGP, tu usuario es: ' + username + 'y tu contrasenha: ' + password2,
                'sgpnoreply@gmail.com',
                [email],
                fail_silently=False,
            )
            user = User.objects.create_user(username=username, first_name=request.POST['nombre'],
                                            email=request.POST['email'],
                                            last_name=request.POST['apellido'], password=request.POST['password'])
            if request.POST.get('es_administrador', False) == 'si':
                user.user_permissions.add(permiso)
                admin = True
            else:
                admin = False
            UserProfile.objects.create(user=user, direccion=request.POST['direccion'],
                                       telefono=request.POST['telefono'],
                                       descripcion=request.POST['descripcion'],
                                       captrabajo=request.POST['captrabajo'], es_administrador=admin)
            mensaje = "Guardado exitoso"

    context = {
        'mensaje':mensaje,
    }
    return render(request, "CrearUsuario.html", context)

def ValidateEmail( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False
def cambiarcontrasena(request):
    '''Proporciona la opcion de cambiar contrasenha del usuario. Solicita previamente la contrasenha anterior para realizar
    el cambio correspondiente. '''
    message1=None
    message2=None
    usuario=request.user
    if request.method == "POST":
        if request.user.is_authenticated():
            passanterior = request.POST['passanterior']
            if not request.user.check_password(passanterior):
                message1='La contrasena anterior no coincide.'
            password1=request.POST['password1']
            password2 = request.POST['password2']
            if password2 != password1:
                message2 = 'Las contrasenas no coinciden'
            if(message1 == None and message2 == None):
                request.user.set_password(password2)
                request.user.save()
                return redirect('login')
                #return render(request, 'index.html', {'mensaje': mensaje})
            else:
                return render(request, 'CambiarContrasena.html', {'message1': message1, 'message2':message2, 'usuario':usuario})
        else:
            return render(request,'login.html',{})
    return render(request, 'CambiarContrasena.html', {'message1': message1, 'message2':message2, 'usuario':usuario})




def listaruser(request):
    '''Esta operacion permite listar todos los usuarios del sistema'''
    usuario = UserProfile.objects.all()
    #if request.method=='POST':
        #if not request.POST['usuarioseleccionado']:
         #   mensaje = "Seleccione un usuario"
           # return render(request, 'SEliminarUser.html', {'usuario': usuario, 'mensaje': mensaje})
       # else:
            #usuario_seleccionado= UserProfile.objects.get(pk=request.POST['usuarioseleccionado'])
        #    return render(request,'EliminarUser.html',{'usuario_seleccionado': usuario_seleccionado})
    return render(request, 'SEliminarUser.html', {'usuario': usuario})

def eliminaruser(request, usuid):
    '''Esta funcionalidad permite la eliminacion logica de un usuario aplicada por  un usuario de tipo administrador.
    La operacion no permite la autoeliminacion, por tanto esta sujeta a determinados permisos y restricciones.
    No puede ser aplicada a un usuario asociado a un proyecto sin cancelar y/o finalizar.'''
    usuario=UserProfile.objects.get(pk=usuid)
    mensaje=None
    if request.method == 'POST':

        lista_pro=Proyecto_User_Rol.objects.filter(usuario=usuario.user.username)
        if lista_pro: #si esta en algun proyecto
            for lista in lista_pro:
                p=Proyecto.objects.get(nombre=lista.proyecto)
                if p.estado=='Ejecutando' or p.estado=='Pendiente':
                    mensaje="No se puede eliminar al usuario porque se encuentra asociado a un proyecto sin cancelar ni finalizar"
                else:
                    usuario.user.is_active=False
                    print (usuario.user.is_active)
                    id=usuario.user_id
                    user=User.objects.get(pk=id)
                    usuario.user.save()
                    user.is_active=False
                   # print "usuario desactivado..."
                   # print user.is_active
                    return redirect('listaruser')
        else:
            usuario.user.is_active = False
            print (usuario.user.is_active)
            id = usuario.user_id
            user = User.objects.get(pk=id)
            usuario.user.save()
            user.is_active = False
            # print "usuario desactivado..."
            # print user.is_active
            return redirect('listaruser')
    return render(request,'EliminarUser.html',{'usuario': usuario, 'mensaje':mensaje})



def modificar_usuario(request):
    '''Esta funcion permite la modificacion de los datos personales de un usuario. La modificacion solo puede ser
    hecha por el mismo usuario. Valida que no exitan dos usuarios con el mismo correo electronico dentro del sistema'''

    mensaje = None
    usuario= request.user
    user=UserProfile.objects.get(user__username=usuario.username)
    if request.method == 'POST':
        #new_user = request.POST.get('username',False)
        new_name = request.POST.get('nombre',False)
        new_lastname = request.POST.get('apellido',False)
        new_location = request.POST.get('direccion',False)
        mail= request.POST.get('email',False)
        new_descripcion=request.POST.get('descripcion',False)
        new_telefono=request.POST.get('telefono',False)
        new_captrabajo=request.POST.get('captrabajo',False)
        #VERIFICAR SI EL USERNAME EXISTE
        #print (new_user)
        #print (usuario.username)
        #print ( usuario.username == new_user)
        #if usuario.username != new_user:
         #    if User.objects.filter(username=new_user):
          #     mensaje = "ERROR: Username Existente"
        #VERIFICAR SI EL EMAIL EXISTE
        if usuario.email != mail:
            if User.objects.filter(email=mail):
                mensaje = "ERROR: Email Existente"
            if not ValidateEmail(mail):
                if mensaje:
                    mensaje +='El Email ingresado es incorrecto'
                else:
                    mensaje = 'El Email ingresado es incorrecto'
        if  not mensaje:
            user =UserProfile.objects.get(user__username=usuario.username)
           # user.user.username=new_user
            user.user.first_name=new_name
            user.user.last_name=new_lastname
            user.direccion=new_location
            user.descripcion=new_descripcion
            user.telefono=new_telefono
            user.captrabajo=new_captrabajo
            user.user.email=mail
            user.user.save()
            user.save()
            mensaje = 'Usuario Modificado Exitosamente.'
    context = {
        'mensaje': mensaje,
        'usuario':user,
    }

    return render(request,'ModificarUsuario.html', context)
