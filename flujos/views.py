"""
Vistas relacionadas con el Modulo Flujos dentro del SGP.
    Las vistas cumplen con las siguientes funciones:
    - Listar Flujos de Proyecto
    - Crear Actividades
    - Crear un Flujo
    - Ver un Fluijo
    - Asignar Activiadades a un Flujo
    - Modificar Actividades de un Flujo
    - Eliminar Actividades de un Flujo
    - Importar un Flujo
    - Confirmar la Importacion de un Flujo
"""

from django.shortcuts import render,redirect
from flujos.models import Flujos,Actividades
from userStory.models import UserStories,tipo_us
from proyectos.models import Proyecto
from GestorProyectos.views import log
# Create your views here.
def listarFlujos_Proyecto(request,proyectoid):
    """
    Lista los Flujos que pertenecen a un proyecto
    :param request: Request del Usuario
    :param proyectoid: identificador de un proyecto
    :return: None
    """
    #obtenemos todos los flujos que pertenecen a un proyecto
    mensaje=None
    mensaje1=None
    flujos = Flujos.objects.filter(proyecto=Proyecto.objects.get(pk=proyectoid))
    if not flujos:
        mensaje = "No existen Flujos creados para este proyecto."
    context={
        'mensaje':mensaje,
        'mensaje1':mensaje1,
        'flujos':flujos,
        'proyectoid':proyectoid,
    }
    return render(request,'listarFlujos.html',context)



def crear_Actividades(request,proyectoid):
    """
    Crea una Actividad dentro de un Proyecto
    :param request: Request de un Usuario
    :param proyectoid: id de un proyecto en el que se creara una actividad
    :return: None
    """
    mensajeError = None
    mensajeExito = None
    proy = Proyecto.objects.get(pk=proyectoid)
    nomp = proy.nombre + '.txt'
    usuario = request.user
    if request.method == 'POST':
        nombreA = request.POST.get('nombreA',)
        #if Actividades.objects.filter(nombre=nombreA):
         #   mensajeError = "Ya existe una Actividad con este nombre."
        if not mensajeError:
            #est1=Estado.objects.create(nombre='POR HACER')
            #est2=Estado.objects.create(nombre='HACIENDO')
            #est3=Estado.objects.create(nombre='HECHO')
            Actividades.objects.create(nombre=nombreA,proyecto=proy,flujo=None)
            mensajeExito = "Creada la Actividad con exito"
            # log
            log(nomp, nombreA, 'Creacion de Actividad', usuario)

    context = {
        'mensajeError':mensajeError,
        'mensajeExito':mensajeExito,
        'proyectoid':proyectoid,
    }
    return render(request,'crearActividades.html',context)
def crearFlujo(request,proyectoid):
    """
    Crea un  Flujo dentro de un Proyecto
    :param request: Request de un Usuario
    :param proyectoid: id de un proyecto en el que se creara un  Flujo
    :return: None
    """
    proy = Proyecto.objects.get(pk=proyectoid)
    nomp = proy.nombre + '.txt'
    usuario = request.user
    lista_tipoUS = tipo_us.objects.all()
    mensajeExito = None
    mensajeError = None
    if not tipo_us.objects.all():
        mensajeError = 'Se necesita tener Tipo de US creados antes de crear un flujo'
    if proy.estado == 'Pendiente' or proy.estado == 'Ejecutando':
        # si el proyecto tiene un estado valido
        if request.method == 'POST':
            nombreF = request.POST.get('nombre', )
            tpUS = tipo_us.objects.filter(nombre=request.POST.get('tpUS', ))
            if Flujos.objects.filter(nombre=nombreF, proyecto=proy):
                mensajeError = "Ya existe un flujo con este nombre"
            if not tpUS:
                if not mensajeError:
                    mensajeError = "Nombre de Tipo de US invalido"
                else:
                    mensajeError += " - Nombre de Tipo de US invalido"
            if not mensajeError:
                tpUS = tipo_us.objects.get(nombre=request.POST.get('tpUS', ))
                Flujos.objects.create(nombre=nombreF, tipoUS=tpUS, proyecto=proy)
                mensajeExito = "Exito al crear el Flujo"
                log(nomp, nombreF, 'Creacion de flujo', usuario)
    else:
        mensajeError = "No se puede crear un flujo para un proyecto Cancelado o Finalizado"
    context = {
        'mensajeExito': mensajeExito,
        'mensajeError': mensajeError,
        'proyectoid': proyectoid,
        'lista_tipoUS': lista_tipoUS,
    }
    return render(request, 'crearFlujo.html', context)
def ver_Flujo(request,idflujo):
    """
    Ver los datos basicos de un Flujo(nombre, lista de acitvidades y tipo de US)
    :param request: Resuqest del Usuario
    :param idflujo: id del Flujo que se quiere ver
    :return:  None
    """

    #obtenemos el flujo
    flujo = Flujos.objects.get(pk=idflujo)
    flujos = Flujos.objects.filter(nombre=flujo.nombre)
    #obtenemos las activiadades del flujo
    actividades = Actividades.objects.filter(flujo=flujo).order_by('id')
    nroAct = cantidadDeActividades(actividades)*3

    list = [] # lista de que guarda los US del Flujo
    for a in actividades:
        users_stories = UserStories.objects.filter(actividad=a)
        for u in users_stories:
            list.append(u)

    context = {
        'Flujo':flujo,
        'lista_flujos':flujos,
        'Actividades':actividades,
        'USs':list,
        'idflujo':idflujo,
        'proyectoid':flujo.proyecto.id,
        'nroA': nroAct,
    }
    return render(request,'verFlujo.html',context)

def asignarActividades_Flujo(request,idflujo):
    """
    Asigna una avtividad al flujo que recibe como parametro
    :param request: Request del Usuario
    :param idflujo: id del flujo al que se le asiganra una actividad
    :return: None
    """
    mensajeError = None
    mensajeExito = None
    mensajeInformativo1 = None
    mensajeInformativo2 = "Cree Actividades para el Flujo previamente seleccionado. El orden de las actividades en el Flujo sigue el orden en que se crean."
    flujo = Flujos.objects.get(pk=idflujo)
    actividades = Actividades.objects.filter(flujo=flujo).order_by('id')
    proy = Proyecto.objects.get(pk=flujo.proyecto_id)
    proy = proy.nombre
    nomp = proy + '.txt'
    usuario = request.user
    print(actividades)
    if not actividades:
        mensajeInformativo1 = "No existen actividades creadas para el flujo. Puede crearlas en la seccion de arriba."
    if request.method == 'POST':
        nombreA = request.POST.get('nombreA',)
        actividad = Actividades.objects.create(nombre=nombreA,proyecto=flujo.proyecto,flujo=flujo)
        actividades = Actividades.objects.filter(flujo=flujo).order_by('id')
        mensajeExito = "Creardo y Asignado Exitosamente."
        log(nomp, flujo.nombre, 'Asignacion de Actividad a Flujo', usuario, 'Actividad Asignada: %s' % nombreA)

    context = {
        'mensajeInformativo1':mensajeInformativo1,
        'mensajeInformativo2': mensajeInformativo2,
        'mensajeExito':mensajeExito,
        'flujo':flujo.nombre,
        'Actividades':actividades,
        'proyectoid':flujo.proyecto.id,
        'nombreProyecto':flujo.proyecto.nombre,
    }
    return render(request,'asignarActividad_Flujo.html',context)

def modificarFlujo(request,idflujo):
    """
    Modificar el Flujo que se recibe como parametro
    :param request: Request del usuario
    :param idflujo: id del flujo cuyos campos y actividades seran modificados
    :return: None
    """
    mensajeError = None
    mensajeExito = None
    mensajeError2 = None
    flujo = Flujos.objects.get(pk=idflujo)
    print (flujo.proyecto.id)
    actividades = Actividades.objects.filter(flujo=flujo).order_by('id')
    proy = Proyecto.objects.get(pk=flujo.proyecto_id)
    proy = proy.nombre
    nomp = proy + '.txt'
    usuario = request.user
    nomf = flujo.nombre
    if not actividades:
        mensajeError2 = "El flujo no tiene Actividades Asignadas."
    if request.method == 'POST':
        nombreF = request.POST.get('nombreF',)
        #tpUS = request.POST.get('tpUS',)
        if flujo.nombre != nombreF:
            if Flujos.objects.filter(nombre=nombreF):
                mensajeError = "Ya existe un Flujo con este nombre."
        #if not tipo_us.objects.filter(nombre=tpUS):
         #   if mensajeError:
          #      mensajeError += " - No existe el tipo de US."
           # else:
            #    mensajeError = "No existe el tipo de US."
        if not mensajeError:
            #tpUS = tipo_us.objects.get(nombre=tpUS)
            flujo.nombre = nombreF
            #flujo.tipoUS = tpUS
            flujo.save()
            mensajeExito = "Cambios Guardados."
            log(nomp, nomf, 'Modificacion de Flujo', usuario)
    context = {
        'mensajeError': mensajeError,
        'mensajeExito':mensajeExito,
        'mensajeError2':mensajeError2,
        'flujo':flujo,
        'Actividades':actividades,
        "proyectoid":flujo.proyecto.id,
    }
    return render(request,'modificarFlujo.html',context)

def eliminarActividad(request,idactividad):
    """
    Desasiganar uan Actividad de un Flujo
    :param request: Request del Usuario
    :param idactividad: id de la actividad que sera desasignada del Flujo al que fue asignado
    :return: None
    """
    actividad = Actividades.objects.get(pk=idactividad)
    flujo = Flujos.objects.get(pk=actividad.flujo.id)
    proy = Proyecto.objects.get(pk=flujo.proyecto_id)
    proy = proy.nombre
    nomp = proy + '.txt'
    usuario = request.user
    if request.method == 'POST':
        boton = request.POST.get('respuesta',)
        print (boton)
        if boton == "si":
            actividad.flujo=None
            actividad.save()
            return redirect('modificarFlujo',flujo.id)
            log(nomp, flujo.nombre, 'Eliminacion de Actividad de Flujo', usuario,'Actividad Eliminada: %s' % actividad.nombre)
        elif boton == "no":
            return redirect('modificarFlujo',flujo.id)
    context = {
        'actividad':actividad,
        'flujo':flujo,
        'idflujo':flujo.id,
        'proyectoid':actividad.proyecto.id,
    }
    return render(request,'eliminarActividad.html',context)

def modificarActividad(request,idactividad):
    """
    Modificar el nombre  de una activiadad recibida como parametro
    :param request: Request del Usuario
    :param idactividad: id de la activaidad que sera modificada
    :return: None
    """
    mensajeError =None
    mensajeExito = None
    actividad = Actividades.objects.get(pk=idactividad)
    flujo = Flujos.objects.get(pk=actividad.flujo.id)
    proy = Proyecto.objects.get(pk=flujo.proyecto_id)
    proy = proy.nombre
    nomp = proy + '.txt'
    usuario = request.user
    if request.method == 'POST':
        nombreA = request.POST.get('nombreA',)
        if actividad.nombre != nombreA:
            if Actividades.objects.filter(nombre=nombreA):
                mensajeError = "Ya existe activiadd con ese nombre"
        if not mensajeError:
            actividad.nombre = nombreA
            actividad.save()
            mensajeExito = "Guardado Exitosamente."
            log(nomp, actividad.nombre, 'Modificacion de Actividad', usuario)
    context = {
        'actividad': actividad,
        'flujo': flujo,
        'idflujo': flujo.id,
        'mensajeError':mensajeError,
        'mensajeExito':mensajeExito,
        'proyectoid':actividad.proyecto.id,
    }
    return render(request, 'modificarActividad.html', context)
def importarFlujo(request,proyectoid):
    """
    Importar un Flujo del sistema y asignar al proyecto recibido como parametro
    :param request: Request del Usuario
    :param proyectoid: id del proyecto en donde se importara el flujo
    :return: None
    """
    mensaje = None
    proyecto = Proyecto.objects.get(pk=proyectoid)
    flujos = Flujos.objects.all()
    if not flujos:
        mensaje = "No existe Flujos en el sistema."
    context = {
        'mensaje':mensaje,
        'proyecto':proyecto,
        'flujos':flujos,
        'proyectoid':proyectoid
    }
    return render(request,'mostrarFlujos_Importar.html',context)
def confirmarImportacion(request,idflujo,idproyecto):
    """
    Confirmar la importacion de un Flujo en dentro del proyecto recibido como parametro
    :param request: Request del Usuario
    :param idflujo: id del flujo que sera importado
    :param idproyecto: id del proyecto en el que sera importado el flujo
    :return: None
    """
    mensaje= None
    nuevoFlujo=None
    flujo = Flujos.objects.get(pk=idflujo)
    actividades = Actividades.objects.filter(flujo=flujo).order_by('id')
    proyecto = Proyecto.objects.get(pk=idproyecto)

    proy = proyecto.nombre
    nomp = proy + '.txt'
    usuario = request.user

    if request.method == 'POST':
        respuesta = request.POST.get('respuesta',)
        if respuesta == "si":
            if Flujos.objects.filter(nombre=flujo.nombre,proyecto=proyecto):
                flujo.nombre+="Importado."
                flujo.nombre+=str(flujo.id)
                print(flujo.nombre)
                nuevoFlujo = Flujos.objects.create(nombre=flujo.nombre,tipoUS=flujo.tipoUS,proyecto=proyecto)
            else:
                nuevoFlujo = Flujos.objects.create(nombre=flujo.nombre, tipoUS=flujo.tipoUS,proyecto=proyecto)
            for a in actividades:
                Actividades.objects.create(nombre=a.nombre,proyecto=proyecto,flujo=nuevoFlujo)
            mensaje = "Flujo importado Correctamente."
            log(nomp, flujo.nombre, 'Importacion de Flujo', usuario)

            return redirect('importarFlujo', idproyecto)
        else:
            return redirect('importarFlujo',idproyecto)

    context = {
        'flujo':flujo,
        'actividades':actividades,
        'proyectoid':idproyecto,
        'mensajeExito':mensaje,
    }
    return render(request,'confirmarImportacion.html',context)

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
        act = Actividades.objects.get(nombre=actividad)
        US.actividad = act
        US.estado='Por Hacer'
        US.save()
        log(nomp, US.nombreUS, 'Cambio de Estado US', usuario,'En flujo:', flujo.nombre)
    contex = {
        'actividades':lista_act,
        'flujo':flujo,
        'proyectoid':flujo.proyecto.id,
        'uStory':US,
        'mensajeExito':mensajeExito,
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
    list_act = Actividades.objects.filter(flujo=flujo).order_by('id')  # se obtiene todos las Actividades del Flujo
    mensaje = None # mensaje a mostrar en pantalla
    user = request.user # usuario que esta trabajando en el flujo
    if request.method == 'POST':
        if request.POST.get('boton',) == 'cambiar': # si el usuario oprimio cambiar estado
            # vemos que estado tiene el US
            estado = US.estado
            if estado == 'Por Hacer':
                US.estado = 'Haciendo'
            elif estado == 'Haciendo':
                US.estado = 'Hecho'
            if US.estado == 'Hecho': # si es el estado hecho
                if US.actividad.nombre != list_act[len(list_act)-1].nombre: # si no estamos en la ultima actividad
                    ActN = retornarActividad(list_act, US.actividad)
                    US.actividad = ActN
                    US.estado = 'Por Hacer'
                else: # si estamos en la ultima actividad no permitimos cambiar de estado y mostramos un mensaje
                    mensaje = "Ya no se pude cambiar de estado el US. Ya se encuentra en el ultimo esado\n Se ha notificado al Scrum Master"

            if not mensaje:
                US.save()
                return redirect('verFlujo', idflujo)
        elif request.POST.get('boton',) == 'retroceder':
            return redirect('retrocederUS', idflujo,idus)
    context = {
        'flujo':flujo,
        'uStory':US,
        'proyectoid':flujo.proyecto.id,
        'mensaje':mensaje,
        'user':user,
    }
    return render(request,'verUS.html',context)

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

def retornarActividad(listaA,actA):

    totalA = len(listaA)
    i = 0
    for a in listaA:
        if a.nombre == actA.nombre:
            if i+1 < totalA:
                return listaA[i+1]
