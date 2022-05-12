''' Vistas para el modelo User Story que incluye la creacion, modificacion,
asignacion a miembros de los mismos'''
from django.shortcuts import render
from proyectos.models import Proyecto_User_Rol, Proyecto
from userStory.models import UserStories
from usuario.models import UserProfile
from tipoUS.models import tipo_us


def crearUS(request,proyectoid):
    '''Crea un nuevo User Story, con los campos requeridos y las comprobaciones
    necesarias para su creacion'''
    mensaje=None
    proyecto=Proyecto.objects.get(pk=proyectoid)
    lista_tipoUS = tipo_us.objects.all()
    if request.method == "POST":
        auxiliar=UserStories()
        nombre= request.POST['nombre']
        tiempo_pla = request.POST['tiempoPla']
        tipous = request.POST['tipoUS']
        valor_negocio = request.POST['v_negocio']
        valor_tecnico = request.POST['v_tecnico']
        prioridad_cliente=request.POST['pc']
        prioridad = (2*float(valor_tecnico)+float(valor_negocio)+float(prioridad_cliente))/4
        #archivo=request.POST['file']
        #PN+PC+2VT/4
        #terminado = request.POST['terminado']


        if not auxiliar.nombre_duplicado(nombre, proyectoid):
            mensaje="El nombre indicado para el US ya existe"

        else:
            UserStories.objects.create(id_proyecto=Proyecto.objects.get(pk=proyectoid), tipoUS=tipo_us.objects.get(nombre=tipous),
                                       nombreUS=nombre, tiempo_planificado=tiempo_pla, valor_negocio= valor_negocio,
                                       valor_tecnico=valor_tecnico,descripcion_corta=request.POST['des_corta'], descripcion_larga = request.POST['des_larga'],
                                       notas=request.POST['notas'],prioridad=prioridad, prioridad_cliente=prioridad_cliente,tiempo_acumulado=tiempo_pla)
            #archivos.objects.create(archivos_adjuntos=archivo, us=us)

            mensaje="US Guardado exitosamente"

    return render(request,'CrearUS.html', {'mensaje': mensaje, 'proyecto':proyecto,'lista_tipoUS':lista_tipoUS})


def listar_US(request, proyectoid):
    ''':param proyectoid: recibe el id del proyecto al que esta asociado el User Story
    Lista todos los User Stories del Proyecto para que puedan ser elegidos por el usuario
    '''
    lista_us = UserStories.objects.filter(id_proyecto=Proyecto.objects.get(pk=proyectoid))
    context = {
        'lista_us': lista_us,
        'proyectoid':proyectoid
    }
    return render(request, 'ListarUserStory.html', context)


def modificarUS(request, ustoryid, proyectoid):
    ''':param ustoryid, proyectoid recibe el identificador del proyecto al que esta asociado el US, y el
    identificador de US que se desea modificar
    Se modifican los campos US que son modificables y se guarda en la base de datos'''
    mensaje = None
    us = UserStories.objects.get(pk=ustoryid)
    if request.method == 'POST':
        valorN=request.POST.get('valorN', False)
        pcliente=request.POST.get('prioriCliente', False)
        valorT=request.POST.get('valorT', False)
        dcorta = request.POST.get('des_corta', False)
        dlarga = request.POST.get('des_larga', False)
        notas = request.POST.get('notas', False)
        te = request.POST.get('tiempo_pla', False)
        prioridad = (2 * float(valorT) + float(valorN) + float(pcliente)) / 4

        if not mensaje:
            us.descripcion_larga = dlarga
            us.valor_negocio=valorN
            us.valor_tecnico=valorT
            us.prioridad_cliente=pcliente
            us.descripcion_corta = dcorta
            us.notas = notas
            us.tiempo_planificado = te
            us.prioridad=prioridad
            us.save()

            mensaje = 'US Modificado Exitosamente.'
    context = {
        'mensaje': mensaje,
        'us': us,
        'proyectoid':proyectoid
    }
    return render(request, 'ModificarUS.html', context)
