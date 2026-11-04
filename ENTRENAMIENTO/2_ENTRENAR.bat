@echo off
setlocal
chcp 65001 >nul
title Entrenar estilo
cd /d "%~dp0.."
set "RAIZ=%cd%"
set "MOTOR=%RAIZ%\motor\ai-toolkit"
set "PY=%MOTOR%\.venv\Scripts\python.exe"

if not exist "%PY%" (
    echo No encuentro el motor instalado. Ejecuta primero 1_INSTALAR.bat
    pause
    exit /b 1
)

echo.
echo ==========================================================
echo   PASO 2 - Entrenamiento del estilo
echo.
echo   Se abren dos ventanas, una por cada RTX 4090:
echo     A ^(rank 16^) en la GPU 0 - estilo mas suave
echo     B ^(rank 32^) en la GPU 1 - trazo mas fiel
echo.
echo   La primera vez descarga FLUX.1-dev ^(unos 35 GB^).
echo   La B arranca cuando la A ya ha cargado el modelo, para
echo   no descargarlo dos veces ni llenar la RAM.
echo.
echo   Cada una tarda unas 2-3 horas. Puedes dejarlo de noche.
echo   Las imagenes de prueba van saliendo en la carpeta SALIDAS.
echo ==========================================================
echo.
pause

"%PY%" "%RAIZ%\ENTRENAMIENTO\crear_configs.py"
if errorlevel 1 goto :error

cd /d "%MOTOR%"
start "Entrenamiento A - GPU 0" cmd /k "set CUDA_VISIBLE_DEVICES=0&& "%PY%" run.py "%RAIZ%\ENTRENAMIENTO\estilo_A_rank16.yaml""

echo Esperando a que la version A cargue el modelo y saque sus primeras pruebas...
echo ^(la primera vez puede tardar bastante por la descarga^)
:esperar
if exist "%RAIZ%\SALIDAS\estilo_A_rank16\samples\*" goto :lanzar_b
timeout /t 30 /nobreak >nul
goto :esperar
:lanzar_b
timeout /t 60 /nobreak >nul

start "Entrenamiento B - GPU 1" cmd /k "set CUDA_VISIBLE_DEVICES=1&& "%PY%" run.py "%RAIZ%\ENTRENAMIENTO\estilo_B_rank32.yaml""

echo.
echo Las dos estan en marcha. Puedes cerrar esta ventana
echo ^(NO cierres las otras dos hasta que terminen^).
pause
exit /b 0

:error
echo.
echo *** Algo ha fallado. Copia el texto de esta ventana y pasaselo a Claude. ***
pause
exit /b 1
