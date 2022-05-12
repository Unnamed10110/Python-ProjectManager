'''Las vistas utilizadas son para creacion, modificacion y asignaciones que tiene un Sprint
en un proyecto dado, tambien se calcula el Backlog'''

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404,redirect
from Sprints.models import Sprint, Sprint_Usuarios
from flujos.models import Flujos,Actividades
from proyectos.models import Proyecto, Proyecto_User_Rol
from userStory.models import UserStories
from usuario.models import UserProfile
from datetime import datetime, date, timedelta
import os
from GestorProyectos.views import log

# BACKLOG
def consultarbacklog(request,proyectoid):
    '''Muestra todos los User Stories del Proyecto (Product Backlog)'''
    backlog=UserStories.objects.filter(id_proyecto=Proyecto.objects.get(pk=proyectoid)).order_by('-prioridad')
    return render (request, 'ConsultarBacklog.html', {'backlog':backlog,'proyectoid':proyectoid})

def sprintbacklog(request, proyectoid):
    '''Muestra los US asociados a los Sprints del proyecto'''
    sprintb=Sprint.objects.filter(id_proyecto=Proyecto.objects.get(pk=proyectoid))
    backlogus=UserStories.objects.filter(id_proyecto=Proyecto.objects.get(pk=proyectoid)).order_by('-prioridad')
    return  render(request, 'SprintBacklog.html', {'sprintb':sprintb,'backlogus':backlogus,'proyectoid':proyectoid})

def ver_us(request, usid, proyectoid):
    '''Muestra los datos del US elegido'''
    uStory=UserStories.objects.get(pk=usid)
    return render(request, 'ver_UserStory.html',{'uStory':uStory, 'proyectoid':proyectoid})
def ver_us2(request, usid, proyectoid):
    '''Muestra los datos del US elegido'''
    uStory=UserStories.objects.get(pk=usid)
    return render(request, 'ver_UserStory2.html',{'uStory':uStory, 'proyectoid':proyectoid})

#SPRINTS

def crear_sprint(request, proyectoid):
    ''' :param proyectoid, el identificador del proyecto que sera asociado al sprint
    Crea un nuevo Sprint asociado a un proyecto con nombre y duracion '''
    mensaje=None
    proyecto=Proyecto.objects.get(pk=proyectoid)
    if request.method == 'POST':
        nombreS = request.POST.get('nombre')
        duracion=request.POST.get('duracion')
        # verifica si el nombre del Sprint ya existe
        sprint = Sprint.objects.filter(id_proyecto=Proyecto.objects.get(pk=proyectoid))
        if verificar_sprint(sprint,nombreS) == True:
            mensaje = "Error: Nombre de Sprint Existente en el Proyecto"
        # verifica si las fechas son validas

        if not mensaje:
            mensaje = 'Sprint Creado Exitosamente.'
            Sprint.objects.create(id_proyecto=Proyecto.objects.get(pk=proyectoid),nombre=nombreS,duracion=duracion,
                                  estado='Pendiente',tiempo_asignado=0.0)
    return render(request,'CrearSprint.html',{'proyecto':proyecto,'mensaje': mensaje,})

def verificar_sprint(sprint,nombreS):
    ''' :param sprint, lista de sprints del proyecto
    :param nombreS, el nombre del sprint a crear
    Verifica que el nombre del Sprint no sea duplicado en el proyecto'''
    for p in sprint:
        if p.nombre == nombreS:
            return True
        return False

def modificar_sprint(request,id_sprint):
    '''Permite la modificacion de un sprint con estado pendiente o en ejecucion.
    Controla la validez de las fechas y la transicion entre estados. '''
    mensaje = None
    sprint = get_object_or_404(Sprint, pk=id_sprint)
    proyectoid = sprint.id_proyecto.id
    if request.method == 'POST':
        #nombre_nuevo = request.POST.get('nombre',False)
        #fecha1_nueva = request.POST.get('FechaInicio',False)
        estado = request.POST.get('estado',False)
        duracion=request.POST.get('duracion',False)
        estado0 = sprint.estado
        #verificar estado
        if estado == '-----------':
            mensaje = " - Estado Invalido"
        if estado0 == 'Pendiente' and estado == 'Finalizado':
            mensaje = "No se puede cambiar el estado de Pendiente a Finalizado"
        if estado0 == 'Ejecutando' and estado == 'Pendiente':
            mensaje = "No se puede cambiar el estado de Ejecutando a Pendiente"
        if estado0 == 'Finalizado':
            mensaje = "El Sprint ha sido Finalizado - No se permiten modificaciones."
        if estado0 == 'Cancelado':
            mensaje='El Sprint fue Cancelado - No se admite modificaciones'
        us = UserStories.objects.filter(sprint=sprint)
        if estado0 == 'Pendiente' and estado == 'Ejecutando':
            if not us:
                if mensaje:
                    mensaje+=" - El sprint no tiene US asignados "
                else:
                    mensaje = "El sprint no tiene US asignados "
            su = Sprint_Usuarios.objects.filter(sprint=sprint.nombre)
            if not su:
                if mensaje:
                    mensaje += " - El sprint no tiene Usuarios asignados "
                else:
                    mensaje = "El sprint no tiene Usuarios asignados "
            flujo=Flujos.objects.filter(sprint=sprint)
            if not flujo:
                if mensaje:
                    mensaje += " - El sprint no tiene Flujos asignados "
                else:
                    mensaje = "El sprint no tiene Flujos asignados "
            ############################################################################
            #obtener todos los sprints del proyecto para verificar que niguno tenga el estado ejecutando
            flag=None
            sprints = Sprint.objects.filter(id_proyecto=sprint.id_proyecto)
            for sps in sprints:
                if sps.id != sprint.id:
                    if sps.estado == 'Ejecutando':
                        flag=1
                        break
            if flag:
                if not mensaje:
                    mensaje = "Ya existe un Sprint en el proyecto que esta Ejecutandose."
                else:
                    mensaje += "- Ya existe un Sprint en el proyecto que esta Ejecutandose."
            ######################################################################

        if (estado == 'Cancelado' or estado == 'Finalizado') and not mensaje:
            for u in us:
                if not u.terminado:
                    if u.terminado == False:
                        u.actividad=None
                        u.estado=None
                        u.sprint = None

        if int(duracion)< sprint.duracion:
            if not mensaje:
                mensaje='La duracion del Sprint no puede ser menor a la duracion actual'
            else:
                mensaje += 'La duracion del Sprint no puede ser menor a la duracion actual'
        if not mensaje:
            sprint.duracion = duracion
            if estado == 'Ejecutando' and estado0 != 'Ejecutando':
                sprint.estado = estado
                sprint.fechaInicio = date.today()
                sprint.fechaFin=validar_domingo_y_sabado(date.today(),duracion)
            else:
                sprint.estado = estado
            sprint.save()
            mensaje = 'Modificacion Exitosa'
            if estado=='Finalizado':
                p=Proyecto.objects.get(id=proyectoid)
                scm=p.scrum_master
                use=User.objects.get(username=scm)
                send_mail(
                    'Finalizacion de Sprint',
                    'Un sprint del que es miembro a finalizado. Sprint finalizado: ' + sprint.nombre,
                    'sgpnoreply@gmail.com',
                    [use.email],
                    fail_silently=False,
                )
    context = {
        'mensaje': mensaje,
        'sprint':sprint,
        'proyectoid': proyectoid,
    }
    return render(request,'ModificarSprint.html',context)

def validar_domingo_y_sabado (fecha, duracion):
    ''':param fecha, la fecha en que se inicia el sprint
    :param duracion, la duracion que tendra el Sprint
    Valida la fecha  que culminara el Sprint, sin incluir sabado y domingo'''
    dias =( 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo' )
    i=1
    d=int(duracion)
    fechaProxima=date.today()
    #fecha1=parse_date(fecha)
    while(i <= d):
        print ("entra en while")
        fechaProxima=fechaProxima + timedelta(days=1)
        print (fechaProxima)
        dia_semana = datetime.weekday(fechaProxima)
        print (dia_semana)
        if dia_semana == 6 or dia_semana == 5:
            i=i-1
        i=i+1;
    return fechaProxima

def listar_sprint(request, proyectoid):
    ''':param recibe el identificador del proyecto
    Muestra la lista de Sprints de un proyecto dado'''
    listar_sprint=Sprint.objects.filter(id_proyecto=Proyecto.objects.get(pk=proyectoid))
    return render(request, 'listarSprint.html', {'listar_sprint': listar_sprint, 'proyectoid': proyectoid})


def elegir_miembro_sprint(request, id_sprint, proyectoid):
    ''':param recibe el id del proyecto y el identificador de sprint
    Muestra todos los usuarios que no estan asociados al Sprint actual, y que pertenezcan
    al proyecto'''
    lista_pro_usu = Proyecto_User_Rol.objects.filter(proyecto=Proyecto.objects.get(pk=proyectoid).nombre)
    lista_usuarios = UserProfile.objects.all()
    Sp = Sprint.objects.get(pk=id_sprint)
    verificar_usuario_en_sprint=Sprint_Usuarios.objects.filter(sprint=Sp.nombre)
    lista=[]
    if lista_pro_usu:
        for proyec in lista_pro_usu:
            for usu in lista_usuarios:
                ban=0
                if verificar_usuario_en_sprint:
                    if usu.user.is_active:
                        if usu.user.username == proyec.usuario:
                            for usuSprint in verificar_usuario_en_sprint:
                                if usuSprint.usuario == usu.user.username:
                                    ban=1
                                    break
                            if ban != 1:
                                lista.append(usu)
                else:
                    if usu.user.is_active:
                        if usu.user.username == proyec.usuario:
                            lista.append(usu)
    context = {
        'Sp': Sp,
        'proyectoid': proyectoid,
        'lista':lista,
        'verificar_usuario_en_sprint':verificar_usuario_en_sprint,
    }
    return render(request, 'ElegirMiembroSprint.html', context)

def asignar_miembro_sprint(request, id_sprint, usuarioid):
    '''Muestra los datos del Usuario a agregar en el Sprint y lo agrega'''
    mensaje=None
    usuario_a_asignar=UserProfile.objects.get(pk=usuarioid)
    Sp=Sprint.objects.get(pk=id_sprint)
    if request.method=='POST':
        send_mail('Te asignaron a un Sprint','Has sido asignado como miembro del Sprint: '+Sp.nombre+'del proyecto: '+Sp.id_proyecto.nombre+'del que eres miembro, dicho Sprint esta '+Sp.estado,'sgpnoreply@gmail.com',[usuario_a_asignar.user.email],fail_silently=False)
        Sprint_Usuarios.objects.create(usuario=usuario_a_asignar.user.username,sprint=Sp.nombre)
        Sp.tiempo_asignado=float(funcion_auxiliar(Sp))
        Sp.save()
        mensaje='Usuario asignado correctamente al Sprint'
    context={
        'usuario_a_asignar':usuario_a_asignar,
        'Sp':Sp,
        'mensaje':mensaje,
        'proyectoid': Sp.id_proyecto.id
    }
    return render(request,'AsignarMiembroSprint.html', context)

def elegir_US_Sprint(request, sprintid, proyectoid):
    '''Lista todos los US del proyecto que no estan en ningun Sprint'''
    lista_us = UserStories.objects.filter(id_proyecto=Proyecto.objects.get(pk=proyectoid))
    Sp=Sprint.objects.get(pk=sprintid)
    horas=Sp.duracion*16 - Sp.tiempo_asignado
    context={
        'lista_us':lista_us,
        'Sp':Sp,
        'horas':horas,
        'proyectoid': proyectoid
    }
    return render(request,'ElegirUSSprint.html',context)


def asignar_US_Sprint(request,uStoryid,sprintid,proyectoid):
    '''Al asignar el US calcula el tiempo asignado del Sprint de la siguiente forma:
    obtiene la sumatoria de todos los US asociados al sprint dividida por la
    sumatoria de la capacidad de trabajo de los usuarios asociados al sprint '''
    mensaje=None
    sprint=Sprint.objects.get(pk=sprintid)
    us=UserStories.objects.get(pk=uStoryid)
    if request.method=='POST':
        us.sprint=sprint
        us.save()
        tAsignado = funcion_auxiliar(sprint)
        if(tAsignado<=sprint.duracion*16):
            print (tAsignado)
            sprint.tiempo_asignado=float(tAsignado)
            print(sprint.tiempo_asignado)
            sprint.save()
            mensaje = 'US asignado al Sprint'
        else:
            us.sprint=None
            us.save()
            mensaje='No puede asignarse este US al Sprint porque la duracion del mismo es rebasada'

    return render(request,'AsignarUSSprint.html',{'us':us, 'mensaje':mensaje,'proyectoid':proyectoid,'sprintid':sprintid})

def funcion_auxiliar(sprint):
    ''':param recibe el sprint a modificar el campo de tiempo asignado
    Calcula el tiempo asignado al sprint de acuerdo a los US asociados y el equipo'''
    capacidad_de_trabajo_total = 0
    tiempo_estimado_us = 0
    lista_users = Sprint_Usuarios.objects.filter(sprint=sprint.nombre)
    lista_ustory = UserStories.objects.filter(sprint=sprint)
    mul=1
    if lista_ustory:
        for lus in lista_ustory:
            tiempo_estimado_us += lus.tiempo_planificado
        if lista_users:
            mul=16
            for users in lista_users:
                user = User.objects.get(username=users.usuario)
                usu = UserProfile.objects.get(user=user)
                usu_rol = Proyecto_User_Rol.objects.get(usuario=usu.user.username, proyecto=sprint.id_proyecto.nombre)
                if usu_rol.rol != 'product_owner':
                    capacidad_de_trabajo_total += usu.captrabajo
    if capacidad_de_trabajo_total == 0:
        capacidad_de_trabajo_total = 1
    #print (float(tiempo_estimado_us) / float(capacidad_de_trabajo_total),"///////")
    return float((float(tiempo_estimado_us) / float(capacidad_de_trabajo_total))*float(mul))



def ListaUS(request, proyectoid, sprintid):
    ''':param recibe el id del proyecto y el identificador del Sprint
    Lista todos lo US asociados al Sprint'''
    lis=[]
    li=[]
    lista_us = UserStories.objects.filter(id_proyecto=Proyecto.objects.get(pk=proyectoid),sprint=Sprint.objects.get(pk=sprintid))
    for i in lista_us:
            if not i.usuario_asignado:
                lis.append(i)
            else:
               li.append(i)
    context = {
        'lis_us': lis,
        'li': li,
        'sprintid': sprintid,
        'proyectoid': proyectoid
    }
    return  render(request, 'ListaUSparaUsuario.html',context)




def elegir_miembro_us(request, ustoryid, proyectoid, sprintid):
    ''':param recibe el id de proyecto, y el id del US
    Se elige el usuario al que va a ser asignado el User Story
    '''
    li=[]
    lista_usu_sprint=Sprint_Usuarios.objects.filter(sprint=Sprint.objects.get(pk=sprintid).nombre)
    lista_pro=Proyecto_User_Rol.objects.filter(proyecto=Proyecto.objects.get(pk=proyectoid).nombre)
    for i in lista_pro:
        for j in lista_usu_sprint:
            if j.usuario==i.usuario and i.rol!='product_owner':
                li.append(UserProfile.objects.get(user=User.objects.get(username=j.usuario)))
    Us=UserStories.objects.get(pk=ustoryid)
    context={
        'Us':Us,
        'li': li,
        'proyectoid': proyectoid,
        'sprintid':sprintid
    }
    return render(request, 'ElegirUsuarioUS.html', context)

def asignar_miembro_us(request, ustoryid, usuarioid, sprintid):
    ''' :param recibe el id de usuario y el id de US a asignar
    Si el Scrum Master esta seguro de asignar el US al dicho usuario, si no esta con sobregarga de trabajo
    se lo asigna y se guarda en la base de datos'''
    mensaje=None
    usuario=UserProfile.objects.get(pk=usuarioid)
    US=UserStories.objects.get(pk=ustoryid)
    auxiliar=UserStories()
    proyecto = Proyecto.objects.get(nombre=US.id_proyecto.nombre)
    if request.method=='POST':
        os.system('pause')
       # print (US.usuario_asignado)
        if not US.usuario_asignado:
            if not auxiliar.asignado_a_user(usuario):  # si es true se puede agregar, sino no se puede
                mensaje = "Este usuario ya tiene demasiado trabajo, el US no puede ser asignado"
        #        print mensaje
            else:
                print (usuario.user.email)
                os.system('pause')
                send_mail('Te asignaron un US',
                          'Te han asignado el US : ' + US.nombreUS + ' del proyecto: ' + US.id_proyecto.nombre +
                          ' para que trabajes por el mismo', 'sgpnoreply@gmail.com',
                          [usuario.user.email], fail_silently=False)
                usuario.trabasignado = usuario.trabasignado + US.tiempo_planificado
                US.usuario_asignado = usuario
                mensaje = "El US ha sido asignado con exito"
                usuario.save()
                print (usuario.user.email)
                os.system('pause')
                US.save()


        else:
            mensaje="Este US ya esta asignado"
    ''' usuario_anterior=US.usuario_asignado
    horas=US.tiempo_planificado-US.tiempo_ejecutado
    usuario_anterior.trabasignado-=horas
    US.usuario_asignado=None
    usuario_anterior.save()
    US.save()
    if not auxiliar.asignado_a_user(usuario):  # si es true se puede agregar, sino no se puede
        mensaje = "Este usuario ya tiene demasiado trabajo, el US no puede ser asignado"
        #print mensaje
    else:
        usuario.trabasignado = usuario.trabasignado + US.tiempo_planificado
        US.usuario_asignado = usuario
        mensaje = "El US ha sido asignado con exito"
        #print mensaje
    '''
    context={
        'usuario':usuario,
        'US':US,
        'mensaje':mensaje,
        'proyectoid': proyecto.id,
        'sprintid':sprintid

    }
    return render(request,'AsignarUS.html', context)


#para flujo
def AsignarFlujoSprint(request,flujoid,sprintid,proyectoid):
    ''':param toma el id del proyecto asociado al flujo, el id del flujo, y el id del sprint
    Agrega el flujo al Sprint'''
    mensaje = None
    sprint = Sprint.objects.get(pk=sprintid)
    flujo = Flujos.objects.get(pk=flujoid)
    if request.method == 'POST':
        flujo.sprint = sprint
        flujo.save()
        mensaje = 'Flujo asignado al Sprint'
    return render(request, 'AsignarFlujoSprint.html',{'flujo': flujo, 'mensaje': mensaje, 'proyectoid': proyectoid, 'sprintid': sprintid, 'sprint':sprint})

def elegir_flujo_sprint(request, sprintid, proyectoid):
    '''Lista todos los Flujos del proyecto que no estan en ningun Sprint'''
    mensaje = None
    lista_flujos = Flujos.objects.filter(proyecto=Proyecto.objects.get(pk=proyectoid), sprint=None)
    lista_asig = Flujos.objects.filter(sprint=Sprint.objects.get(pk=sprintid))
    if not lista_flujos:
        mensaje = "No existen Flujos creados para este proyecto."
    context = {
        'mensaje': mensaje,
        'lista_flujos': lista_flujos,
        'lista_asig': lista_asig,
        'proyectoid': proyectoid,
        'sprintid': sprintid,
    }
    return render(request,'ElegirFlujoSprint.html',context)

##############################################################################################################################################################
##############################################################################################################################################################
###########################################################-----FLUJOS-----####################################################################################
def listarFlujos_Sprint(request,sprintid):
    """
    Lista los Flujos que pertenecen a un sprint
    :param request: Request del Usuario
    :param sprintid: identificador de un sprint
    :return: None
    """
    #obtenemos todos los flujos que pertenecen a un sprint
    mensaje=None
    sprint = Sprint.objects.get(pk=sprintid)
    flujos = Flujos.objects.filter(sprint=sprint)
    if not flujos:
        mensaje = "No existen Flujos creados para este Sprint."
    context={
        'mensaje':mensaje,
        'flujos':flujos,
        'proyectoid':sprint.id_proyecto.id,
        'sprintid':sprintid,
    }
    return render(request,'listarFlujosSprint.html',context)

def ver_FlujoSprint(request,idflujo,idsprint):
    """
    Ver los datos basicos de un Flujo(nombre, lista de actividades y tipo de US)
    :param request: Resquest del Usuario
    :param idflujo: id del Flujo que se quiere ver
    :return:  None
    """

    #obtenemos el flujo
    flujo = Flujos.objects.get(pk=idflujo)
    sprint = Sprint.objects.get(pk=idsprint)
    flujos = Flujos.objects.filter(nombre=flujo.nombre,sprint=sprint)
    #obtenemos las activiadades del flujo
    actividades = Actividades.objects.filter(flujo=flujo).order_by('id')
    nroAct = cantidadDeActividades(actividades)*3

    list = [] # lista de que guarda los US del Flujo
    for a in actividades:
        users_stories = UserStories.objects.filter(actividad=a).order_by('id')
        for u in users_stories:
            print(u.terminado)
            list.append(u)
    list.sort(key=lambda us: us.nombreUS)
    context = {
        'Flujo':flujo,
        'lista_flujos':flujos,
        'Actividades':actividades,
        'USs':list,
        'idflujo':idflujo,
        'proyectoid':flujo.proyecto.id,
        'nroA': nroAct,
        'sprintid':sprint.id,
    }
    return render(request,'verFlujoSprint.html',context)

def asignarUS_Flujo(request,idflujo,sprintid):
    """
    Asigna un User Sotory al flujo que recibe como parametro.
    :param request: Request del Usuario
    :param idflujo: id del flujo alq ue se le asignara los User Stories
    :return: None
    """
    mensajeError = None
    mensajeError1 = None
    mensajeExito = None
    actividades = None
    us = None
    flujo = Flujos.objects.get(pk=idflujo)
    actividades = Actividades.objects.filter(flujo=flujo).order_by('id')
    actividad = primeraActividad(actividades)
    sprint = Sprint.objects.get(pk=sprintid)
    us3 = UserStories.objects.filter(id_proyecto=flujo.proyecto, actividad=actividad,tipoUS=flujo.tipoUS,sprint=sprint).order_by('id')
    for u in us3:
        print("\n")
        print(u.nombreUS)
    if not actividades:
        mensajeError = "No existen Actividades creadas para el Flujo."
    else:
        actividad= primeraActividad(actividades)
        us = UserStories.objects.filter(id_proyecto=flujo.proyecto,actividad=None,tipoUS=flujo.tipoUS,sprint=sprint)
        if not us:
            if mensajeError:
                mensajeError += " - No existen US creados para el proyecto. O ya fueron asignados."
            else:
                mensajeError = "No existen US creados para el proyecto. O ya fueron asignados."
        else:
            if request.method == 'POST':
                nombreUS = request.POST.get('nombreUS',)
                us1 = UserStories.objects.filter(nombreUS=nombreUS,id_proyecto=flujo.proyecto, actividad=None,tipoUS=flujo.tipoUS,sprint=sprint)
                if not us1:
                    mensajeError1 = "No existe el US o ya fue asignado a un Flujo. Escoja uno de la lista de US sin asignar."
                else:
                    us2 = UserStories.objects.get(nombreUS=nombreUS)
                    us2.actividad = actividad
                    us2.estado = 'Por Hacer'
                    us2.save()
                    mensajeExito = "Asignacion Correcta."
                    us = UserStories.objects.filter(id_proyecto=flujo.proyecto, actividad=None,tipoUS=flujo.tipoUS,sprint=sprint)
                    us3 = UserStories.objects.filter(id_proyecto=flujo.proyecto, actividad=actividad,tipoUS=flujo.tipoUS,sprint=sprint)
    context = {
        'mensajeError':mensajeError,
        'mensajeError1':mensajeError1,
        'mensajeExito':mensajeExito,
        'USs1':us,
        'USs2':us3,
        'proyectoid':flujo.proyecto.id,
        'flujo':flujo.nombre,
        'sprintid':sprintid,
    }
    return render(request,'asignarUS_Flujo.html',context)

def retrocederUS(request,idflujo,idus):
    """
    Retroce un US en la actividad que especifica el Scrum Master
    :param request: Request del Usuario
    :param idflujo: id del flujo que sera importado
    :param idus: id del US a retroceder
    :return: None
    """
    flujo=Flujos.objects.get(pk=idflujo)
    lista_act = Actividades.objects.filter(flujo=flujo)
    US = UserStories.objects.get(pk=idus)
    mensajeExito = None
    proyecto = Proyecto.objects.get(pk=flujo.proyecto_id)
    proy = proyecto.nombre
    nomp = proy + '.txt'
    usuario = request.user
    if request.method == 'POST':
        actividad = request.POST.get('actividad',)
        act = Actividades.objects.get(nombre=actividad,flujo=flujo)
        US.actividad = act
        US.estado='Por Hacer'
        US.tiempo_acumulado=US.tiempo_acumulado+0.5*US.tiempo_planificado
        US.usuario_asignado.trabasignado=US.usuario_asignado.trabasignado+0.5*US.tiempo_planificado

        US.save()
        log(nomp, US.nombreUS, 'Cambio de Estado US (Retroceder)', usuario, 'En flujo:', flujo.nombre)
        return redirect('verFlujoSprint', idflujo, flujo.sprint.id)
    contex = {
        'actividades':lista_act,
        'flujo':flujo,
        'proyectoid':flujo.proyecto.id,
        'uStory':US,
        'mensajeExito':mensajeExito,
        'sprintid':US.sprint.id,
    }
    return render(request,'retrocederUS.html',contex)

def verUSParaCambiarEstado(request,idflujo,idus):
    """"
        Cambiar de estado el US que esta en un flujo. Ambos son recibidos en los parametros
        :param request: Request del Usuario
        :param idflujo: id del flujo donde esta el US
        :param idus: id del US a cambiar de estado
        :return: None
    """
    flujo=Flujos.objects.get(id=idflujo)
    US = UserStories.objects.get(id=idus)
    usu=User.objects.get(pk=US.usuario_asignado_id)
    list_act = Actividades.objects.filter(flujo=flujo).order_by('id')  # se obtiene todos las Actividades del Flujo
    mensaje = None # mensaje a mostrar en pantalla
    proyecto = Proyecto.objects.get(pk=flujo.proyecto_id)
    proy = proyecto.nombre
    nomp = proy + '.txt'
    usuario = request.user
    user = request.user # usuario que esta trabajando en el flujo
    if request.method == 'POST':
        notas = request.POST.get('notas',)
        print (notas)
        US.notas = notas
        US.save()
        if request.POST.get('boton',) == 'cambiar': # si el usuario oprimio cambiar estado
            # vemos que estado tiene el US
            estado = US.estado
            if estado == 'Por Hacer':
                US.estado = 'Haciendo'
                log(nomp, US.nombreUS, 'Cambio de Estado US (Avanzar: Haciendo)', usuario, 'En flujo:', flujo.nombre)
            elif estado == 'Haciendo':
                US.estado = 'Hecho'
                if not US.actividad.nombre != list_act[len(list_act) - 1].nombre:  # si estamos en la ultima actividad
                    send_mail('Finalizacion de US',
                              'Un US de su proyecto a finalizaddo : ' + US.nombreUS + ' del proyecto: ' + US.id_proyecto.nombre , 'sgpnoreply@gmail.com',
                              [usu.email], fail_silently=False)
            elif estado == 'Hecho':
                if US.actividad.nombre != list_act[len(list_act) - 1].nombre:  # si no estamos en la ultima actividad
                    US.estado = 'Por Hacer'
                    log(nomp, US.nombreUS, 'Cambio de Estado US (Avanzar: Por Hacer)', usuario, 'En flujo:', flujo.nombre)
                    ActN = retornarActividadSiguiente(list_act, US.actividad)
                    US.actividad = ActN
                else:  # si estamos en la ultima actividad no permitimos cambiar de estado y mostramos un mensaje
                    mensaje = "Ya no se pude cambiar de estado el US. Ya se encuentra en el ultimo esado\n Se ha notificado al Scrum Master"
            if not mensaje:
                US.save()
                return redirect('verFlujoSprint', idflujo,flujo.sprint.id)
        elif request.POST.get('boton',) == 'retroceder':
            return redirect('retrocederUS', idflujo,idus)
        elif request.POST.get('boton',) == 'retrocederUnUS':
            print('entro aqui para retroceder\n')
            # vemos que estado tiene el US
            estado = US.estado
            if estado == 'Por Hacer':
                if primeraActividad(list_act).nombre == US.actividad.nombre: #estamos en la primera actividad en el primer estado
                    mensaje = "Ya no se pude cambiar de estado el US. Se encuetra en el primer Estado del Flujo"
                else: # hay que retroceder de actividad
                    ActN=retornarActividadAnterior(list_act, US.actividad)
                    print(ActN.nombre)
                    US.estado = 'Hecho'
                    US.actividad = ActN
            elif estado == 'Haciendo':
                US.estado = 'Por Hacer'
                log(nomp, US.nombreUS, 'Cambio de Estado US (Retroceder: Por Hacer)', usuario, 'En flujo:', flujo.nombre)
            elif estado == 'Hecho':
                US.estado = 'Haciendo'
                log(nomp, US.nombreUS, 'Cambio de Estado US (Retroceder: Haciendo)', usuario, 'En flujo:',flujo.nombre)
            US.save()
            return redirect('verFlujoSprint', idflujo, flujo.sprint.id)
        elif request.POST.get('boton', ) == 'terminar':
            # si se dio por terminado en US
            return redirect('darPorTerminadoUS',US.id)
    context = {
        'flujo':flujo,
        'uStory':US,
        'proyectoid':flujo.proyecto.id,
        'mensaje':mensaje,
        'user':user,
        'ultimaActividad':list_act[len(list_act)-1],
        'sprintid':flujo.sprint.id,
    }
    return render(request,'verUSSprint.html',context)

def darPorTerminadoUS(request,idus):
    """
    Dar por termiando un US
        :param request: Request del Usuario
        :param idus: id del US a dar pro terminado
        :return: None
    """

    US = UserStories.objects.get(pk=idus)
    iduser =US.usuario_asignado_id
    user=UserProfile.objects.get(user_id=iduser)

    if request.method == 'POST':
        US.terminado = True
        user.trabasignado=user.trabasignado-(US.tiempo_acumulado-US.tiempo_ejecutado)
        US.save()
        return redirect('verFlujoSprint', US.actividad.flujo.id, US.sprint.id)
    return render(request,'darPorTerminadoUS.html',{'US':US})

def primeraActividad(actividades):
    """
    Funcion encargada de encontrar la primera actividad dentro de una lsita de actividades
    :param actividades: lista de actividades
    :return: la primera actividad de lista
    """
    for a in actividades:
        return a
def actividadValida(lista, string):
    for l in lista:
        if l.nombre == string:
            return  False
    return  True
def cantidadDeActividades(act):
    i=0
    for a in act:
        i+=1
    return i

def retornarActividadAnterior(listaA,actA):

    totalA = len(listaA)
    actAnterior=listaA[0]
    for a in listaA:
        if a.nombre == actA.nombre:
            return actAnterior
        actAnterior = a

def retornarActividadSiguiente(listaA,actA):

    totalA = len(listaA)
    i = 0
    for a in listaA:
        if a.nombre == actA.nombre:
            if i+1 < totalA:
                return listaA[i+1]
        i=i+1
#####################################

#destalles sprint
def detalles(request, id_sprint, proyectoid):
    '''Muestra los datos del Sprint elegido'''
    sp = Sprint.objects.get(pk=id_sprint)
    horas = sp.duracion - sp.tiempo_asignado
    usu = Sprint_Usuarios.objects.filter(sprint=sp.nombre)
    us=UserStories.objects.filter(sprint_id=id_sprint)
    flu = Flujos.objects.filter(sprint_id=id_sprint)
    return render(request, 'detsprint.html', {'sp': sp, 'proyectoid': proyectoid, 'horas': horas, 'usu':usu, 'us':us, 'flu':flu})

def detalles2(request, id_sprint, proyectoid):
    '''Muestra los datos del Sprint elegido'''
    sp = Sprint.objects.get(pk=id_sprint)
    horas = sp.duracion - sp.tiempo_asignado
    usu = Sprint_Usuarios.objects.filter(sprint=sp.nombre)
    us=UserStories.objects.filter(sprint_id=id_sprint)
    flu = Flujos.objects.filter(sprint_id=id_sprint)
    return render(request, 'detsprint2.html', {'sp': sp, 'proyectoid': proyectoid, 'horas': horas, 'usu':usu, 'us':us, 'flu':flu})


def asignar_miembro_us(request, ustoryid, usuarioid, sprintid):
    ''' :param recibe el id de usuario y el id de US a asignar
    Si el Scrum Master esta seguro de asignar el US al dicho usuario, si no esta con sobregarga de trabajo
    se lo asigna y se guarda en la base de datos'''
    mensaje=None
    usuario=UserProfile.objects.get(pk=usuarioid)
    US=UserStories.objects.get(pk=ustoryid)
    auxiliar=UserStories()
    proyecto = Proyecto.objects.get(nombre=US.id_proyecto.nombre)
    if request.method=='POST':
        if not US.usuario_asignado:
            if not auxiliar.asignado_a_user(usuario):  # si es true se puede agregar, sino no se puede
                mensaje = "Este usuario ya tiene demasiado trabajo, el US no puede ser asignado"
            else:
                usuario.trabasignado = usuario.trabasignado + (US.tiempo_acumulado-US.tiempo_ejecutado)
                US.usuario_asignado = usuario
                mensaje = "El US ha sido asignado con exito"
                usuario.save()
                US.save()
                send_mail('Te asignaron un US',
                          'Te han asignado el US : ' + US.nombreUS + ' del proyecto: ' + US.id_proyecto.nombre +
                          ' para que trabajes por el mismo', 'sgpnoreply@gmail.com',
                          [usuario.user.email], fail_silently=False)
                return redirect('ListaUS', US.id_proyecto.id,US.sprint.id)

    context={
        'usuario':usuario,
        'US':US,
        'mensaje':mensaje,
        'proyectoid': proyecto.id,
        'sprintid':sprintid
    }
    return render(request,'AsignarUS.html', context)

def desasignarUS(request, ustoryid, usuarioid, sprintid):
    ''' :param recibe el id de usuario y el id de US a desasignar'''
    mensaje=None
    US=UserStories.objects.get(pk=ustoryid)
    usu = UserProfile.objects.get(pk=US.usuario_asignado.pk)
    proyecto = Proyecto.objects.get(nombre=US.id_proyecto.nombre)
    if request.method=='POST':
            usu.trabasignado = usu.trabasignado  - (US.tiempo_acumulado -US.tiempo_ejecutado)
            US.usuario_asignado = None
            mensaje = "El US ha sido desasignado con exito"
            usu.save()
            US.save()
            return redirect('ListaUS', US.id_proyecto.id,US.sprint.id)
    context={
        'usu':usu,
        'US':US,
        'mensaje':mensaje,
        'sprintid':sprintid,
        'proyectoid': proyecto.id,
    }
    return render(request,'desasignarUS.html', context)
