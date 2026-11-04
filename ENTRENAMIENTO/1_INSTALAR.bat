@echo off
setlocal
chcp 65001 >nul
title Instalar motor de entrenamiento
cd /d "%~dp0.."
set "RAIZ=%cd%"
set "MOTOR=%RAIZ%\motor\ai-toolkit"

echo.
echo ==========================================================
echo   PASO 1 - Instalacion del motor de entrenamiento
echo   Tarda bastante la primera vez: descarga unos 10 GB.
echo ==========================================================
echo.

where git >nul 2>&1
if errorlevel 1 goto :sin_git

if exist "%MOTOR%\run.py" goto :ya_clonado
echo Descargando AI Toolkit...
if not exist "%RAIZ%\motor" mkdir "%RAIZ%\motor"
git clone https://github.com/ostris/ai-toolkit.git "%MOTOR%"
if errorlevel 1 goto :error
:ya_clonado

cd /d "%MOTOR%"

REM --- uv + Python, igual que el instalador oficial (todo queda dentro de la carpeta motor) ---
set "PATH=%MOTOR%\.uv;%PATH%"
set "UV_PYTHON_INSTALL_DIR=%MOTOR%\.uv\python"
where uv.exe >nul 2>&1
if not errorlevel 1 goto :tiene_uv
echo Descargando uv...
powershell -NoProfile -ExecutionPolicy ByPass -Command "$env:UV_INSTALL_DIR = Join-Path '%MOTOR%' '.uv'; $env:UV_NO_MODIFY_PATH = '1'; irm https://astral.sh/uv/install.ps1 | iex"
where uv.exe >nul 2>&1
if errorlevel 1 goto :error
:tiene_uv

if not exist "%UV_PYTHON_INSTALL_DIR%" uv python install 3.12
set "PY="
for /f "delims=" %%P in ('uv python find 3.12') do set "PY=%%P"
if not defined PY goto :error

echo.
echo Instalando PyTorch y dependencias para tus RTX 4090...
"%PY%" -m manager install
if errorlevel 1 goto :error

REM --- Token de Hugging Face (FLUX.1-dev requiere aceptar su licencia) ---
if exist "%MOTOR%\.env" findstr /b "HF_TOKEN=" "%MOTOR%\.env" >nul 2>&1 && goto :fin

echo.
echo ==========================================================
echo   Falta una cosa: el permiso para descargar FLUX.1-dev
echo.
echo   1. Crea una cuenta gratis en https://huggingface.co
echo   2. Entra en https://huggingface.co/black-forest-labs/FLUX.1-dev
echo      y pulsa el boton para aceptar la licencia.
echo   3. Ve a https://huggingface.co/settings/tokens
echo      Create new token, tipo "Read", y copialo.
echo ==========================================================
echo.
set /p "TOKEN=Pega aqui el token (empieza por hf_) y pulsa Enter: "
if "%TOKEN%"=="" goto :error
>>"%MOTOR%\.env" echo HF_TOKEN=%TOKEN%
echo Token guardado.

:fin
echo.
echo ==========================================================
echo   Instalacion terminada. Ahora ejecuta 2_ENTRENAR.bat
echo ==========================================================
pause
exit /b 0

:sin_git
echo No encuentro Git. Instalalo desde https://git-scm.com/download/win
echo (todo por defecto, siguiente, siguiente) y vuelve a ejecutar este archivo.
pause
exit /b 1

:error
echo.
echo *** Algo ha fallado. Copia el texto de esta ventana y pasaselo a Claude. ***
pause
exit /b 1
