from django.shortcuts import render,get_object_or_404,redirect
from proyectos.forms import ProyectoForm
from proyectos.models import Proyecto, Proyecto_User_Rol
from django.contrib.auth.models import User
from datetime import date
from dateutil.parser import parse as parse_date
from usuario.models import UserProfile
import os
from Sprints.models import Sprint
def crear_proyecto(request):
    '''Crea un nuevo proyecto si se cumplen ciertas condiciones'''
    mensaje=None
    if request.method == 'POST':
        form =  ProyectoForm(request.POST)
        nombreP = request.POST.get('nombre',)
        fecha1 = request.POST.get('FechaInicio',)
        fecha2 = request.POST.get('FechaFin',)
        scrum_master = request.POST.get('scrum',)
        # verifica si el proyecto ya existe
        proyecto = Proyecto.objects.all()
        if verficar_proyecto(proyecto,nombreP) == True:
            mensaje = "Error: Nombre de Proyecto Existente"
        # verifica si las fechas son validas
        if verificar_fechas(fecha1, fecha2) == 1:
            if mensaje:
                mensaje += " - Fechas incorrectas"
            else:
                mensaje = "Error: Fechas Incorrectas"
        # verifica si el scrum master es valido
        if not User.objects.filter(username=scrum_master):
            if mensaje:
                mensaje += " - Scrum Master no existe"
            else:
                mensaje = "Error: Scrum Master no existe"
        if not mensaje:
            mensaje = 'Proyecto Creado Exitosamente.'
            Proyecto.objects.create(nombre=request.POST['nombre'],fechaInicio=request.POST['FechaInicio'],scrum_master=scrum_master,fechaFin=request.POST['FechaFin'],estado='Pendiente')
            Proyecto_User_Rol.objects.create(usuario=scrum_master, proyecto=request.POST['nombre'], rol='scrum_master')
    context = {
        'mensaje': mensaje,
    }
    return render(request,'CrearProyecto.html',context)
def verficar_proyecto(proyecto,nombreP):
    ''' :param recibe la lista de proyectos y el nombre de proyecto a crear
    Verifica que no haya nombres de proyectos duplicados'''
    for p in proyecto:
        if p.nombre == nombreP:
            return  True
        return False

def modificar_proyecto(request,id_proyecto):
    ''' :param recibe el identificador de proyecto por el que se esta trabajando
    Se puede modificar los campos de proyecto'''
    mensaje = None
    mensaje2=None
    proyecto = get_object_or_404(Proyecto, pk=id_proyecto)
    #fianterior = proyecto.fechaInicio.strftime("%d/%m/%y")
    #ffanterior = proyecto.fechaFin.strftime("%d/%m/%y")
    fianterior = proyecto.fechaInicio
    fi1=fianterior.strftime('%Y')
    fi2 = fianterior.strftime('%m')
    fi3 = fianterior.strftime('%d')

    ffanterior = proyecto.fechaFin
    ff1 = ffanterior.strftime('%Y')
    ff2 = ffanterior.strftime('%m')
    ff3 = ffanterior.strftime('%d')
    if request.method == 'POST':
        fecha2_nueva = request.POST.get('FechaFin',False)
        if proyecto.estado=='Ejecutando':
            fecha1_nueva = proyecto.fechaInicio
            #if verificar_fechas(proyecto.fechaFin.strftime('%d/%m/%Y'),fecha2_nueva)==1:
            dt = parse_date(fecha2_nueva)
            if dt.date() < date.today():
                #print ('hoy',dt.strftime('%d/%m/%Y'),'--',date.today().strftime('%d/%m/%Y'))
                #os.system('pause')
                mensaje = "Fechas Incorrectas"
        else:
            fecha1_nueva = request.POST.get('FechaInicio', False)
            if verificar_fechas(fecha1_nueva,fecha2_nueva)==1:
                mensaje = "Error: Fechas Incorrectas"
        estado = request.POST.get('estado',False)
        estado0= proyecto.estado
        #verficar fechas
        #if verificar_fechas(fecha1_nueva, fecha2_nueva) == 1:
        #    mensaje = "Error: Fechas Incorrectas"

        #verificar estado
        if estado == '-----------':
            if mensaje:
                mensaje += " - Estado Invalido"
            else:
                mensaje = "Error: Estado incorrecto"
        if estado0 == 'Pendiente' and estado == 'Finalizado':
            #print ("------------- No puede cambiar el estado de Pendiente a Finalizado ")\
            mensaje = "No puede cambiar el estado de Pendiente a Finalizado"
        if estado0 == 'Ejecutando' and estado == 'Pendiente':
            mensaje = "No puede cambiar el estado de Ejecutando a Pendiente"
        if estado0 == 'Finalizado':
            # un proyecto Finalizado no puede ser modificado

            mensaje = "El proyecto ha sido Finalizado - No se permiten modificaciones."
        if estado0 == 'Cancelado':
            mensaje='El proyecto ha sido Cancelado - No se permiten modificaciones'
        #################################################################################################################
        #################################################################################################################

        if estado == 'Finalizado' and estado0 == 'Ejecutando':
            # obtenemos los sprints del proyecto
            sprints = Sprint.objects.filter(id_proyecto=proyecto)
            # verificamos que ninguno este ejecutando o finalizado
            flag = None
            for sp in sprints:
                if sp.estado == "Ejecutando" or sp.estado == "Pendiente":
                    if mensaje:
                        mensaje += "- No se puede Finalizar el Proyecto, aun existe Sprints Ejecutandose o Pendientes."
                    else:
                        mensaje = "No se puede Finalizar el Proyecto, aun existe Sprints Ejecutandose o Pendientes."
                    flag = 1
                    break
            if not flag:
                return redirect('confirmarFoC', proyecto.id, estado)
        if estado == 'Cancelado':
            return redirect('confirmarFoC', proyecto.id, estado)
        ###################################################################################

        if not mensaje:
            if estado=='Ejecutando' and estado0 != 'Ejecutando':
                k=parse_date(fecha1_nueva)
                if k.strftime('%Y/%m/%d') != date.today().strftime('%Y/%m/%d'):
                    mensaje='Debe cambiar la fecha de inicio al dia de hoy para que el proyecto pueda ejecutarse'
                else:

                    proyecto.fechaInicio = fecha1_nueva
                    proyecto.fechaFin = fecha2_nueva
                    proyecto.estado = estado
                    #print (fecha2_nueva)
                    #os.system('pause')
                    proyecto.save()
                    mensaje2 = "Proyecto modificado exitosamente"
            else:
                proyecto.fechaInicio = fecha1_nueva
                proyecto.fechaFin = fecha2_nueva
                proyecto.estado = estado
                #print (fecha2_nueva)
                #os.system('pause')
                proyecto.save()
                mensaje2 = "Proyecto modificado exitosamente"
    context = {
        'mensaje': mensaje,
        'proyecto':proyecto,
        'proyectoid': id_proyecto,
        'mensaje2':mensaje2,
        'fi1':fi1,
        'fi2': fi2,
        'fi3': fi3,
        'ff1': ff1,
        'ff2': ff2,
        'ff3': ff3,
    }
    return render(request,'ModificarProyecto.html',context)

def verificar_fechas(fecha1,fecha2):
    ''':param recibe dos fechas: una de inicio y fin
    Verifica que la fecha de inicio no sea mayor a la fecha fin'''
    dt=parse_date(fecha2)
    if fecha1 >= fecha2:
        return 1
    if dt.date() < date.today():
        return 1
    return 0


def elegir_proyecto(request):
    '''Selecionamos el proyecto donde queremos trabajar'''
    lista_proyectos = Proyecto.objects.all()
    lista_nombres = Proyecto_User_Rol.objects.filter(usuario=request.user)

    context = {
        'lista_proyectos': lista_proyectos,
        'lista_nombres': lista_nombres,
    }
    return render(request, 'listarProyectos.html', context)

def asignar_usuario_proyecto(request, id_proyecto):
    ''':param recibe el identificador de proyecto al que se le asignara un usuario
    Asigna un usuario elegido al proyecto'''
    mensaje = None
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lista_usuarios = User.objects.all()
    pur = Proyecto_User_Rol.objects.all()
    if request.method == 'POST':
        nombreU = request.POST.get('nombreU')
        rolU = request.POST.get('rol')
        user = User.objects.filter(username=nombreU)
        # VERIFICAR USUARIO SI ES VALIDO

        try:
            u0=User.objects.get(username=nombreU)
            if u0.is_active == False:
                mensaje = "Error: El usuario esta inactivo. No puede ser asignado al proyecto"
        except:
            mensaje = "Error: Usuario incorrecto"
        user_profile = UserProfile.objects.filter(user=user)
        if not user:
            mensaje = "Error: Usuario incorrecto"
        else:
            try:
                pur = Proyecto_User_Rol.objects.get(usuario=nombreU, proyecto=proyecto.nombre)
                if pur:
                    mensaje = "Error: Usuario ya fue asociado a este proyecto"
                pe= get_object_or_404(Proyecto, pk=id_proyecto)
                if pe.estado=="Finalizado":
                    mensaje = "Error: Proyecto finalizado"
            except:
                print ("--------")

        if not mensaje:
            mensaje = "Asignado con exito"
            Proyecto_User_Rol.objects.create(usuario=user.get(username=nombreU).get_username(),proyecto=proyecto.nombre,rol=rolU)
    context = {
        'lista_usuarios': lista_usuarios,
        'mensaje': mensaje,
        'proyectoid': id_proyecto,
        'pur':pur,
    }
    return render(request, 'AsignarUserProyecto.html', context)

################################################################################################
################################################################################################

def confirmarCancelacion_Finalizacion(request,proyectoid,nuevo_estado):
    """
    Confirmar la cancelacion o finalizacion de un proyecto
    :param request: Request del Usuario
    :param proyectoid: identificador de un proyecto
    :param nuevo_estado: estado o Cancelado o Finalizado
    :return: None
    """

    mensaje = None
    #obtenemos el proyecto
    proyecto = Proyecto.objects.get(pk=proyectoid)
    if nuevo_estado == "Finalizado":
        mensaje = "Aun pueden existir USs que no fueron terminados en el proyecto, estos ya no se podran ejecutar, igual desea Finalizar el proyecto?"
    else:
        mensaje = "Si cancela el Proyecto todos las demas entidades quedaran canceladas, US, Sprints y Flujos. Desea realmente Cancelar el Proyecto?"
    if request.method == "POST":
        resp = request.POST.get("respuesta",)
        if resp == 'SI':
            proyecto.estado = nuevo_estado
            proyecto.save()
        return redirect('ver_proyecto',proyecto.id)
    context= {
        'mensaje':mensaje,
        'proyectoid':proyecto.id,
    }
    return render(request,'confirmarFinalizacion_Cancelacion.html',context)
