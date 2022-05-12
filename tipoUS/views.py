'''
views del modulo tipoUS
    -se definen los metodos de creacion de tipoUS.
'''
from django.shortcuts import render

# Create your views here.
from tipoUS.forms import tipo_usForm
from tipoUS.models import tipo_us


def crear_tipo_us(request, proyectoid):
    '''crea el tipo de user story con un nombre dado que debe ser unico en el sistema'''
    mensaje=None
    if request.method == 'POST':
        form =  tipo_usForm(request.POST)
        nombret = request.POST.get('nombre',)
        # verifica si el tipo_us ya existe
        tipo = tipo_us.objects.all()
        if verficar_tipo_us(tipo,nombret) == True:
            mensaje = "Error: Tipo de Historia de Usuario Existente"
        if not mensaje:
            mensaje = 'Tipo de Historia de Usuario Creado Exitosamente.'
            tipo_us.objects.create(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'])
    else:
        form = tipo_usForm()
    context = {
        'form': form,
        'mensaje': mensaje,
        'proyectoid':proyectoid,
    }
    return render(request,'Crear_Tipo_US.html',context)


def verficar_tipo_us(tipo,nombret):
    '''el nombre del tipous debe ser unico'''
    for t in tipo:
        if t.nombre == nombret:
            return  True
        return False
