#!/bin/bash

# UTF-8 para evitar problemas con emojis
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de impresión
print_message() { echo -e "${GREEN}$1${NC}"; }
print_warning() { echo -e "${YELLOW}$1${NC}"; }
print_error()   { echo -e "${RED}$1${NC}"; }
print_info()    { echo -e "${BLUE}$1${NC}"; }

# Verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Limpiar si el script se interrumpe
cleanup() {
    print_warning "\n⚠️  Setup interrumpido. Limpiando..."
    if [ -d "venv" ] && [ ! -f "venv/.keep" ]; then
        rm -rf venv
    fi
    exit 1
}
trap cleanup SIGINT SIGTERM

echo
echo "========================================"
print_message "🤖 HEALTH IA"
echo "========================================"

# Detectar sistema operativo
IS_MACOS=false
IS_LINUX=false

if [[ "$OSTYPE" == "darwin"* ]]; then
    IS_MACOS=true
    print_info "🧠 Sistema detectado: macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    IS_LINUX=true
    print_info "🐧 Sistema detectado: Linux"
else
    print_error "❌ Sistema operativo no compatible"
    exit 1
fi

echo
print_info "🔍 Verificando instalación de Python..."
if ! command_exists python3; then
    print_error "❌ ERROR: Python 3 no está instalado"

    if $IS_MACOS; then
        print_info "Instalando Python 3 con Homebrew..."
        if ! command_exists brew; then
            print_info "Instalando Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python3 || {
            print_error "❌ No se pudo instalar Python 3"
            exit 1
        }
    else
        print_info "Por favor instala Python 3:"
        print_info "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
        print_info "  CentOS/RHEL: sudo yum install python3 python3-pip"
        print_info "  Arch: sudo pacman -S python python-pip"
        exit 1
    fi
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
print_message "✅ Python encontrado: $PYTHON_VERSION"

print_info "🔍 Verificando pip..."
if ! command_exists pip3; then
    print_error "❌ ERROR: pip3 no está disponible"
    print_info "Intenta con: sudo apt install python3-pip"
    exit 1
fi

print_info "🔍 Verificando módulo venv..."
if ! python3 -c "import venv" 2>/dev/null; then
    print_error "❌ ERROR: El módulo venv no está disponible"
    print_info "Instala con: sudo apt install python3-venv"
    exit 1
fi

if [ ! -d "logs" ]; then
    mkdir -p logs
    print_message "📁 Directorio de logs creado"
fi

# Verificar o recrear entorno virtual
if [ -d "venv" ]; then
    if [ -f "venv/bin/activate" ]; then
        print_warning "⚠️  Ya existe un entorno virtual. ¿Deseas recrearlo? (s/N)"
        read -r RECREATE
        if [[ $RECREATE =~ ^[Ss]$ ]]; then
            print_info "🗑️  Eliminando entorno virtual existente..."
            rm -rf venv
        else
            print_message "✅ Usando entorno virtual existente"
        fi
    else
        print_warning "⚠️  Entorno virtual dañado. Se recreará..."
        rm -rf venv
    fi
fi

if [ ! -d "venv" ]; then
    print_info "🔧 Creando entorno virtual..."
    if ! python3 -m venv venv; then
        print_error "❌ ERROR: No se pudo crear el entorno virtual"
        exit 1
    fi
fi

echo
print_info "🔄 Activando entorno virtual..."
source venv/bin/activate

# Verificación real de activación
if [[ -z "$VIRTUAL_ENV" ]]; then
    print_error "❌ ERROR: No se pudo activar el entorno virtual"
    exit 1
fi

echo
print_info "📦 Actualizando pip..."
"$VIRTUAL_ENV/bin/python" -m pip install --upgrade pip

echo
print_info "📦 Instalando dependencias..."
if ! pip install -r requirements.txt; then
    print_error "❌ ERROR: No se pudieron instalar las dependencias"
    print_info "Verifica tu conexión a internet y el archivo requirements.txt"
    exit 1
fi

sudo apt update
sudo apt install -y libgl1

echo
print_info "⚙️  Configurando el proyecto..."

# Crear archivo config.py si no existe
if [ ! -f "config.py" ]; then
    print_info "📝 Creando archivo de configuración..."
    cp config.example.py config.py
    print_warning "⚠️  Edita config.py si deseas personalizar la configuración"
fi

# Detectar número de núcleos del sistema
CPU_CORES=$(getconf _NPROCESSORS_ONLN)

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    print_info "📝 Creando archivo .env..."
    cat > .env << EOF
# Configuración de Health IA

# Frontend
DEBUG=True
HOST=127.0.0.1
PORT=8050

# Configuración llama.cpp
MODEL_PATH=RUTA/AL/MODELO/llama-2-7b-chat.Q4_K_M.gguf
LLAMA_N_THREADS=$CPU_CORES
LLAMA_N_BATCH=256
LLAMA_N_CTX=2048
EOF

    print_warning "⚠️  Edita .env y cambia MODEL_PATH por la ruta real de tu modelo GGUF"
    print_warning "ℹ️  Si no tienes el modelo, puedes descargarlo desde:"
    echo "     https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF"
    echo "     Versión recomendada: llama-2-7b-chat.Q4_K_M.gguf"
fi
echo
echo "========================================"
print_message "✅ SETUP COMPLETADO EXITOSAMENTE"
echo "========================================"
echo
print_info "🚀 Para ejecutar la aplicación:"
print_info "   1. Activa el entorno virtual: source venv/bin/activate"
print_info "   2. Ejecuta la app: python app/main.py"
print_info "   3. Abre tu navegador en: http://127.0.0.1:8050"
echo
print_info "📚 Para más información, consulta el README.md"
echo
print_warning "⚠️  RECUERDA: Edita config.py o .env con tu API key de OpenAI"
echo

# Crear script de ejecución rápida
cat > run_app.sh << 'EOF'
#!/bin/bash
echo "🤖 Iniciando Health IA..."
source venv/bin/activate
python app/app_modular.py
EOF

chmod +x run_app.sh
print_message "✅ Script de ejecución rápida creado: ./run_app.sh"

echo
print_info "🎉 ¡Todo listo! Puedes ejecutar ./run_app.sh para iniciar la aplicación"
