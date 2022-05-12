"""GestorProyectos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from GestorProyectos.views import micuenta, administracion, ver_proyecto
from Sprints.views import crear_sprint, asignar_miembro_sprint, listar_sprint, modificar_sprint, consultarbacklog, \
    sprintbacklog, ver_us, ver_us2, elegir_miembro_us, asignar_miembro_us, ListaUS, elegir_flujo_sprint, \
    AsignarFlujoSprint,listarFlujos_Sprint,darPorTerminadoUS,retrocederUS,asignarUS_Flujo,verUSParaCambiarEstado,ver_FlujoSprint,detalles,detalles2
from Sprints.views import asignar_US_Sprint, elegir_miembro_sprint, elegir_US_Sprint
from flujos.views import crearFlujo, crear_Actividades, ver_Flujo, asignarActividades_Flujo, modificarFlujo, \
    eliminarActividad, modificarActividad, confirmarImportacion, listarFlujos_Proyecto,importarFlujo
from login.views import login_page, salir, homepage
from tipoUS.views import crear_tipo_us
from userStory.views import listar_US, crearUS, modificarUS
from usuario.views import registrousuario, cambiarcontrasena, eliminaruser, listaruser, modificar_usuario
from proyectos.views import crear_proyecto,modificar_proyecto,elegir_proyecto,asignar_usuario_proyecto
from django.core.mail import send_mail, send_mass_mail
from datetime import date
from dateutil.parser import parse as parse_date
from Sprints.views import *
from proyectos.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login_page, name="login"),
    url(r'^login/$', salir, name="logout"),
    url(r'^micuenta/$', micuenta, name="micuenta"),
    url(r'^principal/$', homepage, name="homepage"),
    url(r'^administracion/$', administracion, name="administracion"),

    #usuarios
    url(r'^usuarios/$', registrousuario, name="crearusuario"),
    url(r'^cambiocontrasena/$',cambiarcontrasena, name="cambiarcontra"),
    url(r'^listaruser/$', listaruser, name="listaruser"),
    url(r'^(?P<usuid>[0-9]+)/eliminarusuario/$', eliminaruser, name="eliminarusuario"),
    url(r'^moduser/$', modificar_usuario, name="moduser"),

    #Proyectos
    url(r'^elegirproyec/$', elegir_proyecto, name="elegirProyecto"),
    url(r'^proyectos/$', crear_proyecto, name="crearproyecto"),
    url(r'^modProyecto/(?P<id_proyecto>[0-9]+)/$', modificar_proyecto, name="modificarProyecto"),
    url(r'^resProyecto/(?P<proyectoid>[0-9]+)/$', ver_proyecto, name="ver_proyecto"),
	url(r'^asigUser/(?P<id_proyecto>[0-9]+)/$', asignar_usuario_proyecto, name="asignar_usuario_proyecto"),
    ##########################################################################################################################
    url(r'^asigUser/(?P<proyectoid>[0-9]+)/(?P<nuevo_estado>[a-z A-Z]+)/$', confirmarCancelacion_Finalizacion,name="confirmarFoC"),

    # User Story
    url(r'^listarUS/(?P<proyectoid>[0-9]+)/$', listar_US, name="ListarUS"),
    url(r'^crearUS/(?P<proyectoid>[0-9]+)/$', crearUS, name="CrearUS"),
    url(r'^modifUS/(?P<ustoryid>[0-9]+)/(?P<proyectoid>[0-9]+)/$', modificarUS, name="ModificarUS"),

    # sprint
    url(r'^listarSprint/(?P<proyectoid>[0-9]+)/$', listar_sprint, name="ListarSprint"),
    url(r'^crearSprint/(?P<proyectoid>[0-9]+)/$', crear_sprint, name="CrearSprint"),
    url(r'^modifSprint/(?P<id_sprint>[0-9]+)/$', modificar_sprint, name="ModificarSprint"),
    url(r'^detSprint/(?P<id_sprint>[0-9]+)/(?P<proyectoid>[0-9]+)/$', detalles, name="DetSprint"),
    url(r'^detSprint2/(?P<id_sprint>[0-9]+)/(?P<proyectoid>[0-9]+)/$', detalles2, name="DetSprint2"),
    url(r'^asignarMiembroSprint/(?P<id_sprint>[0-9]+)/(?P<usuarioid>[0-9]+)/$',asignar_miembro_sprint, name="AsignarMiembroSprint"),
    url(r'^elegirMiembroSprint/(?P<id_sprint>[0-9]+)/(?P<proyectoid>[0-9]+)/$', elegir_miembro_sprint, name="ElegirMiembroSprint"),
    url(r'^elegirUSSprint/(?P<sprintid>[0-9]+)/(?P<proyectoid>[0-9]+)/$', elegir_US_Sprint, name="ElegirUSSprint"),
    url(r'^asignarUSSprint/(?P<uStoryid>[0-9]+)/(?P<sprintid>[0-9]+)/(?P<proyectoid>[0-9]+)/$', asignar_US_Sprint, name="AsignarUSSprint"),
    # flujos y sprint
    url(r'^VerCambiarEstUS/(?P<idflujo>[0-9]+)/(?P<idus>[0-9]+)/$', verUSParaCambiarEstado, name="verUScambiarEstado"),
    url(r'^RetrocederUS/(?P<idflujo>[0-9]+)/(?P<idus>[0-9]+)/$', retrocederUS, name="retrocederUS"),
    url(r'^FlujosdelSprint/(?P<sprintid>[0-9]+)/$', listarFlujos_Sprint, name="listarFlujosSprint"),
    url(r'^DatosFlujo/(?P<idflujo>[0-9]+)/(?P<idsprint>[0-9]+)/$', ver_FlujoSprint, name="verFlujoSprint"),
    url(r'^AsigUSFlujo/(?P<idflujo>[0-9]+)/(?P<sprintid>[0-9]+)/$', asignarUS_Flujo, name="asignarUSFlujo"),
    url(r'^TerminarUS/(?P<idus>[0-9]+)/$', darPorTerminadoUS, name="darPorTerminadoUS"),


    url(r'^AsignarFlujoSprint/(?P<flujoid>[0-9]+)/(?P<sprintid>[0-9]+)/(?P<proyectoid>[0-9]+)/$', AsignarFlujoSprint,name="AsignarFlujoSprint"),
    url(r'^ElegirFlujoSprint/(?P<sprintid>[0-9]+)/(?P<proyectoid>[0-9]+)/$', elegir_flujo_sprint,name="ElegirFlujoSprint"),


    url(r'^listaUS/(?P<proyectoid>[0-9]+)/(?P<sprintid>[0-9]+)/$', ListaUS, name="ListaUS"),
    url(r'^elegirMiembroUS/(?P<ustoryid>[0-9]+)/(?P<proyectoid>[0-9]+)/(?P<sprintid>[0-9]+)/$', elegir_miembro_us, name="ElegirMiembroUS"),
    url(r'^asignarUS/(?P<ustoryid>[0-9]+)/(?P<usuarioid>[0-9]+)/(?P<sprintid>[0-9]+)/$', asignar_miembro_us, name="AsignarMiembroUS"),
    url(r'^desasignarUS/(?P<ustoryid>[0-9]+)/(?P<usuarioid>[0-9]+)/(?P<sprintid>[0-9]+)/$', desasignarUS,name="desasignarUS"),

    #tipoUS
    url(r'^crearTUS/(?P<proyectoid>[0-9]+)/$', crear_tipo_us, name="CrearTipoUS"),

    #backlog
    url(r'^consultarBacklog/(?P<proyectoid>[0-9]+)/$', consultarbacklog, name="ConsultarBacklog"),
    url(r'^sprintBacklog/(?P<proyectoid>[0-9]+)/$', sprintbacklog, name="SprintBacklog"),
    url(r'^verUS/(?P<usid>[0-9]+)/(?P<proyectoid>[0-9]+)/$', ver_us, name="VerUS"),
    url(r'^verUS2/(?P<usid>[0-9]+)/(?P<proyectoid>[0-9]+)/$', ver_us2, name="VerUS2"),

    # Flujos
    url(r'^Flujos/(?P<proyectoid>[0-9]+)/$', listarFlujos_Proyecto, name="listarFlujos"),
    url(r'^CrearFlujo/(?P<proyectoid>[0-9]+)/$', crearFlujo, name="crearFlujos"),
    url(r'^CrearActividad/(?P<proyectoid>[0-9]+)/$', crear_Actividades, name="crearActividad"),
    url(r'^DatosFlujo/(?P<idflujo>[0-9]+)/$', ver_Flujo, name="verFlujo"),
    url(r'^AsigActFlujo/(?P<idflujo>[0-9]+)/$', asignarActividades_Flujo, name="asignarActividades"),
    url(r'^ModificarFlujo/(?P<idflujo>[0-9]+)/$', modificarFlujo, name="modificarFlujo"),
    url(r'^EliminarAct/(?P<idactividad>[0-9]+)/$', eliminarActividad, name="eliminarActividad"),
    url(r'^ModAct/(?P<idactividad>[0-9]+)/$', modificarActividad, name="modificarActividad"),
    url(r'^ImportFlujo/(?P<proyectoid>[0-9]+)/$', importarFlujo, name="importarFlujo"),
    url(r'^ConfFlujo/(?P<idflujo>[0-9]+)/(?P<idproyecto>[0-9]+)/$', confirmarImportacion, name="confirmarImportacion"),

]
from userStory.models import UserStories
from usuario.models import UserProfile
from django.contrib.auth.models import User
import os
import threading
def temporizador():
    '''Metodo de tipo hilo para verificar y recalcular los tiempos de los objetos con estado Ejecutando.'''
    us=UserStories.objects.filter(estado = 'Haciendo')
    #print us.count()
    for var in us:
        #print ('us:',var.nombreUS,'estado:',var.estado)
        if var.estado=='Haciendo':
            var.tiempo_ejecutado=var.tiempo_ejecutado+0.0028
            var.save()
            #(var.usuario_asignado_id)
            if var.usuario_asignado_id:
                uid=var.usuario_asignado_id
                #usu = User.objects.get(pk=uid)
                usu=UserProfile.objects.get(pk=uid)
                e=User.objects.get(pk=uid)
                print(usu.trabasignado)
                #os.system('pause')
                if var.tiempo_ejecutado>= var.tiempo_acumulado:

                    var.tiempo_acumulado=var.tiempo_acumulado+(var.tiempo_planificado/2)
                    usu.trabasignado=usu.trabasignado+(var.tiempo_planificado/2)
                    if var.tiempo_acumulado > var.tiempo_ejecutado:
                        send_mail(
                            'Tiempo de User Story',
                            'El User Story a su cargo a superado el tiempo planificado. Nombre del User Story: ' + var.nombreUS,
                            'sgpnoreply@gmail.com',
                            [e.email],
                            fail_silently=False,
                        )
                    usu.save()




    threading.Timer(10.0, lambda: temporizador()).start()

temporizador()



from proyectos.models import Proyecto
from Sprints.models import Sprint
def emailn():
    '''Metodo de tipo hilo para notificaciones.'''
    p=Proyecto.objects.all()
    sp=Sprint.objects.all()
    for a in p:
        scm=a.scrum_master
        usu=User.objects.get(username=a.scrum_master)

        fecha1= a.fechaInicio
        #print (fecha1)
        hoy=date.today()
        #print (hoy)
        #dt = parse_date(fecha1)
        #os.system('pause')

        if fecha1 == hoy:
            send_mail(
                'Proyecto iniciado',
                'Su proyecto a iniciado. Usted es Scrum Master en el proyecto: ' + a.nombre ,
                'sgpnoreply@gmail.com',
                [usu.email],
                fail_silently=False,
            )
        fecha2=a.fechaFin
        if fecha2 == hoy:
            send_mail(
                'Fecha de finalizacion de proyecto',
                'Su proyecto ha alcanzado su fecha de finalizacion. Usted es Scrum Master en el proyecto: ' + a.nombre,
                'sgpnoreply@gmail.com',
                [usu.email],
                fail_silently=False,
            )
    hoy = date.today()
    for b in sp:
        if b.fechaFin==hoy:
            pid=Proyecto.objects.get(pk=b.id_proyecto_id)
            scm=pid.scrum_master
            scm=User.objects.get(username=scm)
            send_mail(
                'Fecha de finalizacion de sprint',
                'Su sprint ha alcanzado su fecha de finalizacion. Sprint con fecha actual: ' + sp.nombre,
                'sgpnoreply@gmail.com',
                [scm.email],
                fail_silently=False,
            )




    threading.Timer(86400.0, lambda: emailn()).start()

emailn()