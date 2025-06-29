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
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python encontrado: %PYTHON_VERSION%

:: Verificar si pip está disponible
echo 🔍 Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: pip no está disponible
    pause
    exit /b 1
)

:: Crear directorio de logs si no existe
if not exist "logs" mkdir logs

:: Verificar si ya existe un entorno virtual
if exist "venv" (
    echo Ya existe un entorno virtual. ¿Deseas recrearlo? (S/N) :
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
    echo ❌ ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)

:activate_venv
echo.
echo 🔄 Activando entorno virtual...
call venv\Scripts\activate
if errorlevel 1 (
    echo ❌ ERROR: No se pudo activar el entorno virtual
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
    echo ❌ ERROR: No se pudieron instalar las dependencias
    echo Verifica tu conexión a internet y el archivo requirements.txt
    pause
    exit /b 1
)

echo.
echo ⚙️  Configurando el proyecto...

:: Crear archivo de configuración si no existe
if not exist "config.py" (
    echo 📝 Creando archivo de configuración...
    copy config.example.py config.py
    echo ⚠️  IMPORTANTE: Edita config.py y añade tu API key de OpenAI
)

:: Crear archivo .env si no existe
if not exist ".env" (
    echo 📝 Creando archivo .env...
    echo # Configuración del Asistente Médico Inteligente > .env
    echo OPENAI_API_KEY=tu_clave_api_de_openai_aqui >> .env
    echo DEBUG=True >> .env
    echo HOST=127.0.0.1 >> .env
    echo PORT=8050 >> .env
    echo ⚠️  IMPORTANTE: Edita .env y añade tu API key de OpenAI
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
echo ⚠️  RECUERDA: Edita config.py o .env con tu API key de OpenAI
echo.
pause 