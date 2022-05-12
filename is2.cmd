@echo off 
color 0f
:inicio
cls
echo -- Despliegue
echo -------------
echo 1-) Iniciar repositorio
echo 2-) Clonar proyecto   
echo 3-) Actualizar repositorio (Del master remoto)    
echo 4-) Historial de proyecto
echo 5-) Ejecutar proyecto (Modo desarrollo)
echo 6-) Crear usuario  (automaticamente)
echo 7-) Crear base de datos / Actualizar modelos
echo 8-) Prueba unitaria
echo 9-) Documentacion de codigo
echo 10-) Ejecutar proyecto (Modo produccion)
echo -------------
echo 11-) Salir
echo -------------
echo.

set /p var=Seleccione una opcion [1-6]: 
if "%var%"=="1" goto op1
if "%var%"=="2" goto op2
if "%var%"=="3" goto op3
if "%var%"=="4" goto op4
if "%var%"=="5" goto op5
if "%var%"=="6" goto op6
if "%var%"=="7" goto op7
if "%var%"=="8" goto op8
if "%var%"=="9" goto op9
if "%var%"=="10" goto op10
if "%var%"=="11" goto salir

::Mensaje de error, validación cuando se selecciona una opción fuera de rango
echo. El numero "%var%" no es una opcion valida...
echo.
pause
echo.
goto inicio

:op1
    echo.
    echo. 1-) Iniciar repositorio (Entorno de Desarrolo)
    echo.
		start cmd /k "cd c:\ & cd gestorproyectos & cd scripts & activate & cd.. & git init & echo. Inicializado:  &color 0f & echo. Repositorio y Entorno de desarrollo"
		
    echo.
    pause 
    goto inicio

:op2
    echo.
    echo. 2-) Clonar proyecto   
    echo.
        start cmd /k "cd c:\ & cd gestorproyectos & cd scripts & activate & cd.. & git init & git clone  https://gitlab.com/Sbritos/GestorProyectos.git & cd gestorproyectos & echo. Repositorio listo... & color 0f"
		
    echo.
    pause
    goto inicio
    goto inicio

:op3
    echo.
    echo. 3-) Actualizar repositorio (Del master remoto)    
    echo.
        start cmd /k "cd c:\ & cd gestorproyectos & cd scripts & activate & cd.. & git init & git pull --rebase https://gitlab.com/Sbritos/GestorProyectos.git  & echo. Repositorio actualizado...  &color 0f & pause &exit"
		start cmd /k "cd c:\ & cd gestorproyectos & cd scripts & activate & cd.. & git init &git pull --tags&git pull it01 & git checkout it01 & git branch --all"
		 
    echo.
    pause
    goto inicio
    
:op4
    echo.
	cls
    echo. 4-) Historial de proyecto
    echo.
		cmd /k " echo. Historial... &cd c:\ &color 0f& cd gestorproyectos & git shortlog -n -e -s &pause&exit"
		cmd /k "cls& echo. Historial... &cd c:\ &color 0f& cd gestorproyectos & git shortlog -n -e & pause&exit"
		cmd /k "cls& echo. Historial... &cd c:\ &color 0f& cd gestorproyectos & git log --oneline --decorate&pause&exit"
		cmd /k "cls& echo. Historial... &cd c:\ &color 0f& cd gestorproyectos & git log --graph & exit"
	
		
		
    echo.
    pause
    goto inicio

:op5
    echo.
    echo. 5-) Ejecutar proyecto (Modo desarrollo)
    echo.
        start cmd /k "color 0f&start http://localhost:8000 & cd c:\ & cd gestorproyectos & cd scripts & activate & cd.. & python manage.py runserver --settings=GestorProyectos.settings.development&pause&exit"
		
    echo.
    pause
    goto inicio

:op6     
    echo.
    echo. 6-) Crear usuario  (automaticamente)
    echo.
        cmd /k "cd c:\ & cd gestorproyectos & echo from django.contrib.auth.models import User; User.objects.create_superuser('user4', 'user4@gmail.com', 'user4') | python manage.py shell --settings=GestorProyectos.settings.development&color 0f&echo. --------&exit"
		cmd /k "cd c:\ & cd gestorproyectos & echo from django.contrib.auth.models import User; User.objects.create_superuser('user5', 'user5@gmail.com', 'user5') | python manage.py shell --settings=GestorProyectos.settings.production&color 0f&echo. --------&exit"
		
    echo.
    pause
    goto inicio
	
:op7   
    echo.
	cls
    echo. 7-) Crear base de datos / Actualizar modelos
    echo.
        cmd /k "color 0f & cd c:\ & cd gestorproyectos & cd scripts & activate & cd.. & python manage.py migrate --settings=GestorProyectos.settings.development&exit"
		cmd /k "color 0f & cd c:\ & cd gestorproyectos & cd scripts & activate & cd.. & python manage.py makemigrations --settings=GestorProyectos.settings.development&exit"
		cmd /k "color 0f & cd c:\ & cd gestorproyectos & cd scripts & activate & cd.. & python manage.py migrate --settings=GestorProyectos.settings.production&exit"
		cmd /k "color 0f & cd c:\ & cd gestorproyectos & cd scripts & activate & cd.. & python manage.py makemigrations --settings=GestorProyectos.settings.production&exit"
		
		
    echo.
    pause
    goto inicio

:op8
    echo.
	cls
    echo. 8-) Prueba unitaria
    echo.
        cmd /k "color 0f& echo. - - Funcion - Login (Unit Test) - - & echo. 		- Datos de prueba:& echo. 			- Usuario= User1& echo. 			- Contrasena= User1 & pause & cd c:\ & cd gestorproyectos & cd scripts & activate & cd.. & python manage.py test --settings=GestorProyectos.settings.development&exit"
		
    echo.
    pause
    goto inicio
	
:op9
    echo.
	cls
    echo. 9-) Documentacion de codigo
    echo.
        cmd /k "echo. Documentacion....&cd C:\GestorProyectos\Docs & start index.html&exit"
		
    echo.
    pause
    goto inicio

:op10
    echo.
	cls
    echo. 10-) Ejecutar proyecto (Modo produccion)
    echo.
        start cmd /k "color 0f& cd c:\ & cd gestorproyectos & cd scripts & activate & cd.. &start http://127.60.60.8:8000/ 	& python manage.py runserver 127.60.60.8:8000 --settings=GestorProyectos.settings.production&pause&exit"
		
    echo.
    pause
    goto inicio
	
:salir
    @cls&exit
	

	