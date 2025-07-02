@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 🤖 ASISTENTE MÉDICO INTELIGENTE
echo ========================================
echo Setup automático para Windows
echo.

:: Verificar si Python está instalado
echo 🔍 Verificando instalación de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python desde: https://python.org
    pause
    exit /b 1
)

:: Verificar versión de Python
for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python encontrado: %PYTHON_VERSION%

:: Verificar versión mínima de Python (ej. 3.10 <= x <= 3.11)
setlocal enabledelayedexpansion
for /f "tokens=1-3 delims=." %%a in ("%PYTHON_VERSION%") do (
    set /a MAJOR=%%a
    set /a MINOR=%%b
)

if !MAJOR! LSS 3 (
    echo ❌ ERROR: Se requiere Python 3.10 o superior
    echo ⚠️  Por favor instala Python 3.10 o 3.11, se le sugiere esta version: https://www.python.org/downloads/release/python-3119/
    pause
    exit /b 1
)

if !MAJOR! EQU 3 (
    if !MINOR! LSS 10 (
        echo ❌ ERROR: Se requiere Python 3.10 o superior
        echo ⚠️  Por favor instala Python 3.10 o 3.11, se le sugiere esta version: https://www.python.org/downloads/release/python-3119/
        pause
        exit /b 1
    )

    if !MINOR! GTR 11 (
        echo ❌ ERROR: Python 3.13 no es compatible con TensorFlow ni otras librerías importantes
        echo ⚠️  Por favor instala Python 3.10 o 3.11, se le sugiere esta version: https://www.python.org/downloads/release/python-3119/
        pause
        exit /b 1
    )
)
endlocal

:: Verificar si pip está disponible
echo 🔍 Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: pip no está disponible
    pause
    exit /b 1
)
echo ✅ pip encontrado

:: Crear directorio de logs si no existe
if not exist "logs" mkdir logs

:: Verificar si ya existe un entorno virtual
echo 🔍 Verificando si ya existe un entorno virtual
if exist "venv" (
    echo Ya existe un entorno virtual. ¿Deseas recrearlo? (S/N^)
    set /p RECREATE=
    if /i "%RECREATE%"=="S" (
        echo 🗑️  Eliminando entorno virtual existente...
        rmdir /s /q venv
    ) else (
        echo ✅ Usando entorno virtual existente
        goto :activate_venv
    )
)

echo.
echo 🔧 Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)

:activate_venv
echo.
echo 🔄 Activando entorno virtual...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

echo.
echo 📦 Actualizando pip...
python -m pip install --upgrade pip

echo.
echo 📦 Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    echo Verifica tu conexión a internet y el archivo requirements.txt
    pause
    exit /b 1
)

echo.
echo ⚙️  Configurando el proyecto...

:: Crear archivo de configuración si no existe
if not exist "config.py" (
    echo Creando archivo de configuración...
    copy config.example.py config.py
    echo IMPORTANTE: Edita config.py y añade tu API key de OpenAI
)

:: Crear archivo .env
if not exist ".env" (
    echo Creando archivo .env...
    (
        echo # Configuración del frontend
        echo DEBUG=true
        echo HOST=127.0.0.1
        echo PORT=8000
        echo.
        echo # Configuración general de los asistentes
        echo MODEL_PATH=C:/Users/tu_usuario/llama3/llama-2-7b-chat.Q4_K_M.gguf
        echo LLAMA_N_THREADS=%CORES%
        echo LLAMA_N_BATCH=256
        echo LLAMA_N_CTX=2048
    ) > .env
)


echo.
echo ========================================
echo ✅ SETUP COMPLETADO EXITOSAMENTE
echo ========================================
echo.
echo 🚀 Para ejecutar la aplicación:
echo    1. Activa el entorno virtual: venv\Scripts\activate
echo    2. Ejecuta la app: python app/main.py
echo    3. Abre tu navegador en: http://127.0.0.1:8050
echo.
echo 📚 Para más información, consulta el README.md
echo.

:: Instrucciones adicionales para el usuario
echo.
echo ⚠️  Si usas Windows, asegúrate de tener instalado Visual Studio Build Tools:
echo    https://visualstudio.microsoft.com/visual-cpp-build-tools/
echo.
echo 💾 Descarga el modelo GGUF (recomendado):
echo    Llama 2 7B Chat Q4_K_M (compatible con llama.cpp):
echo    https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q4_K_M.gguf
echo.
echo 👉 Guarda el archivo en: C:/Users/tu_usuario/llama3/
echo.
echo ⚠️  RECUERDA: Edita config.py o .env
echo.
pause 