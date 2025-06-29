# 🚀 Scripts de Setup Automático

Este directorio contiene scripts para configurar automáticamente el **Asistente Médico Inteligente** en diferentes sistemas operativos.

## 📋 Scripts Disponibles

### 🪟 Windows
- **`setup.bat`** - Setup completo para Windows
- **`run_app.bat`** - Ejecución rápida de la aplicación

### 🐧 Linux y 🍎 macOS
- **`setup.sh`** - Setup completo para Linux y macOS
- **`run_app.sh`** - Ejecución rápida de la aplicación


## 🚀 Instalación Rápida

### Windows
```bash
# Ejecutar setup automático
setup.bat

# Ejecutar aplicación
run_app.bat
```

### Linux/macOS
```bash
# Dar permisos de ejecución
chmod +x setup.sh run_app.sh

# Ejecutar setup automático (Linux)
./setup.sh

# Ejecutar aplicación
./run_app.sh
```

## 🔧 Qué Hacen los Scripts

### Setup Scripts
1. **Verificación de Prerrequisitos**
   - ✅ Python 3.8+ instalado
   - ✅ pip disponible
   - ✅ Módulo venv disponible
   - ✅ Homebrew (solo macOS)

2. **Creación del Entorno**
   - 🔧 Crear entorno virtual
   - 📦 Actualizar pip
   - 📦 Instalar dependencias

3. **Configuración del Proyecto**
   - 📝 Crear archivo config.py
   - 📝 Crear archivo .env
   - 📁 Crear directorio de logs

4. **Scripts Adicionales**
   - 🚀 Crear script de ejecución rápida
   - 🔧 Configurar alias (macOS)

### Run Scripts
1. **Verificaciones**
   - ✅ Entorno virtual existe
   - ✅ Dependencias instaladas
   - 🔄 Activación automática

2. **Ejecución**
   - 🚀 Iniciar aplicación
   - 📱 Mostrar URL de acceso
   - 🛑 Manejo de interrupciones

## ⚠️ Requisitos Previos

### Windows
- Python 3.8+ instalado desde [python.org](https://python.org)
- pip incluido con Python

### Linux
- Python 3.8+ y pip3
- Módulo venv
- Comandos de instalación:
  ```bash
  # Ubuntu/Debian
  sudo apt install python3 python3-pip python3-venv
  
  # CentOS/RHEL
  sudo yum install python3 python3-pip
  
  # Arch
  sudo pacman -S python python-pip
  ```

### macOS
- Homebrew (se instala automáticamente si no está)
- Python 3.8+ (se instala automáticamente si no está)

## 🔍 Solución de Problemas

### Error: "Python no está instalado"
- **Windows**: Descarga desde [python.org](https://python.org)
- **Linux**: Usa el gestor de paquetes de tu distribución
- **macOS**: El script instalará Python automáticamente

### Error: "pip no está disponible"
- **Windows**: Reinstala Python marcando "Add to PATH"
- **Linux**: `sudo apt install python3-pip`
- **macOS**: `brew install python3`

### Error: "Módulo venv no disponible"
- **Linux**: `sudo apt install python3-venv`
- **macOS**: `brew install python3`

### Error: "No se pudieron instalar las dependencias"
- Verifica tu conexión a internet
- Actualiza pip: `python -m pip install --upgrade pip`
- Intenta instalar manualmente: `pip install -r requirements.txt`

### Error: "No se pudo activar el entorno virtual"
- Elimina el entorno virtual: `rm -rf venv`
- Ejecuta el setup nuevamente

## 📝 Configuración Manual

Si prefieres configurar manualmente:

1. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

2. **Activar entorno virtual**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables**
   ```bash
   cp config.example.py config.py
   # Editar config.py con tu API key
   ```

5. **Ejecutar aplicación**
   ```bash
   python app/main.py
   ```

## 🎯 Comandos Útiles

### Verificar instalación
```bash
# Verificar Python
python --version

# Verificar pip
pip --version

# Verificar entorno virtual
echo $VIRTUAL_ENV  # Linux/macOS
echo %VIRTUAL_ENV% # Windows
```

### Limpiar instalación
```bash
# Eliminar entorno virtual
rm -rf venv

# Eliminar archivos de configuración
rm config.py .env

# Reinstalar desde cero
./setup_linux.sh  # o setup_windows.bat
```

## 📞 Soporte

Si encuentras problemas:

1. Verifica que cumples los requisitos previos
2. Revisa los mensajes de error en la consola
3. Consulta la sección de solución de problemas
4. Crea un issue en el repositorio con los detalles del error

---

**¡Los scripts están diseñados para hacer la instalación lo más sencilla posible! 🎉** 