# 🤖 Health IA

Plataforma inteligente para diagnóstico preliminar y apoyo médico en zonas rurales, desarrollada en la Hackatón Deeppunk 2025.

## 📋 Descripción

Health IA es una aplicación web que combina procesamiento de lenguaje natural (PLN) y visión por computadora para proporcionar análisis médico asistido. La plataforma está diseñada para ayudar a profesionales de la salud en zonas rurales o con recursos limitados.

### 🎯 Características Principales

- **Análisis de Síntomas**: Evaluación inteligente de síntomas del paciente
- **Procesamiento de Imágenes Médicas**: Análisis de radiografías, resonancias y otras imágenes
- **Diagnóstico Asistido**: Sugerencias de diagnóstico basadas en IA
- **Interfaz Web Intuitiva**: Dashboard moderno y fácil de usar
- **Agente Médico Inteligente**: Sistema basado en Langchain/CrewAI

## 🏗️ Estructura del Proyecto

```
asistente-medico-inteligente/
│
├── 🚀 Scripts de Setup Automático
│   ├── setup_windows.bat      # Setup automático para Windows
│   ├── setup_linux.sh         # Setup automático para Linux
│   ├── setup_macos.sh         # Setup automático para macOS
│   ├── run_app.bat            # Ejecución rápida Windows
│   └── SETUP_SCRIPTS.md       # Documentación de scripts
│
├── app/                       # Archivos Dash y componentes del frontend
│   ├── layout.py             # Layout principal de la aplicación
│   ├── callbacks.py          # Funciones de callback para interactividad
│   └── main.py               # Aplicación principal para ejecutar
│
├── agents/                    # Agente médico (Langchain / CrewAI)
│   └── agente_medico.py      # Implementación del agente médico
│
├── vision/                    # Procesamiento de imágenes y exámenes
│   └── procesar_imagen.py    # Análisis de imágenes médicas
│
├── prompts/                   # Prompts personalizados para PLN
│   └── diagnostico.txt       # Prompt para diagnóstico médico
│
├── data/                      # Dataset de ejemplo, imágenes, PDFs
│   └── README.md             # Documentación de datos
│
├── requirements.txt           # Lista de librerías necesarias
├── config.example.py          # Archivo de configuración de ejemplo
├── README.md                  # Instrucciones del proyecto
└── .gitignore                # Archivos a ignorar en Git
```

## 🚀 Instalación

### 🎯 Instalación Automática (Recomendada)

Para una instalación rápida y automática, usa los scripts de setup:

#### 🪟 Windows
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/asistente-medico-inteligente.git
cd asistente-medico-inteligente

# Ejecutar setup automático
setup_windows.bat

# Ejecutar aplicación
run_app.bat
```

#### 🐧 Linux
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/asistente-medico-inteligente.git
cd asistente-medico-inteligente

# Dar permisos de ejecución
chmod +x setup_linux.sh

# Ejecutar setup automático
./setup_linux.sh

# Ejecutar aplicación
./run_app.sh
```

#### 🍎 macOS
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/asistente-medico-inteligente.git
cd asistente-medico-inteligente

# Dar permisos de ejecución
chmod +x setup_macos.sh

# Ejecutar setup automático
./setup_macos.sh

# Ejecutar aplicación
./run_app.sh
```

**Los scripts automáticos:**
- ✅ Verifican prerrequisitos (Python, pip, etc.)
- ✅ Crean entorno virtual automáticamente
- ✅ Instalan todas las dependencias
- ✅ Configuran archivos de configuración
- ✅ Crean scripts de ejecución rápida

### 📋 Instalación Manual

Si prefieres configurar manualmente:

#### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

#### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/asistente-medico-inteligente.git
   cd asistente-medico-inteligente
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   # Crear archivo .env
   cp .env.example .env
   
   # Editar .env con tus claves API
   OPENAI_API_KEY=tu_clave_api_aqui
   ```

## 🏃‍♂️ Uso

### Ejecutar la Aplicación

#### 🚀 Con Scripts Automáticos (Recomendado)
```bash
# Windows
run_app.bat

# Linux/macOS
./run_app.sh
```

#### 📝 Manualmente
1. **Activar el entorno virtual**
   ```bash
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

2. **Ejecutar la aplicación**
   ```bash
   python app/main.py
   ```

3. **Abrir en el navegador**
   - Ve a: `http://127.0.0.1:8050`
   - La aplicación se abrirá automáticamente

### Funcionalidades

#### 📝 Análisis de Síntomas
1. En la sección "Ingresa los síntomas del paciente"
2. Escribe una descripción detallada de los síntomas
3. Haz clic en "Analizar"
4. Revisa los resultados y recomendaciones

#### 🖼️ Análisis de Imágenes
1. En la sección "Subir imagen médica"
2. Arrastra y suelta una imagen o haz clic para seleccionar
3. La imagen se procesará automáticamente
4. Revisa el análisis y las anomalías detectadas

## 🔧 Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# API Keys
OPENAI_API_KEY=tu_clave_api_de_openai

# Configuración de la aplicación
DEBUG=True
HOST=127.0.0.1
PORT=8050

# Configuración de modelos
MODEL_NAME=gpt-4
TEMPERATURE=0.1
```

### Configuración de Modelos

Los modelos se pueden configurar en:
- `agents/agente_medico.py` - Para el agente médico
- `vision/procesar_imagen.py` - Para el procesamiento de imágenes

## 🧪 Testing

### Ejecutar Tests
```bash
pytest tests/
```

### Ejecutar Tests con Cobertura
```bash
pytest --cov=app --cov=agents --cov=vision tests/
```

## 📚 Documentación

### API Reference

#### Agente Médico
```python
from agents.agente_medico import AgenteMedico

# Crear instancia del agente
agente = AgenteMedico(api_key="tu_api_key")

# Realizar diagnóstico
resultado = agente.diagnosticar("Dolor de cabeza intenso, náuseas")
```

#### Procesador de Imágenes
```python
from vision.procesar_imagen import ProcesadorImagenMedica

# Crear procesador
procesador = ProcesadorImagenMedica()

# Analizar imagen
resultado = procesador.analizar_imagen_medica("ruta/a/imagen.jpg")
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución

- Sigue las convenciones de código (PEP 8)
- Añade tests para nuevas funcionalidades
- Actualiza la documentación cuando sea necesario
- Verifica que todos los tests pasen antes de hacer commit

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## ⚠️ Descargo de Responsabilidad

**IMPORTANTE**: Este software es solo para fines educativos y de asistencia médica. No debe utilizarse como sustituto de la evaluación médica profesional. Siempre consulta con un profesional de la salud calificado para obtener un diagnóstico definitivo y tratamiento apropiado.

## 🎯 Referencia Rápida

### 🚀 Comandos Esenciales

```bash
# Setup automático (elegir según tu sistema)
setup_windows.bat          # Windows
./setup_linux.sh           # Linux
./setup_macos.sh           # macOS

# Ejecutar aplicación
run_app.bat                # Windows
./run_app.sh               # Linux/macOS

# Manual (si no usas scripts automáticos)
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
python app/main.py
```

### 📁 Archivos Importantes

- **`setup_*.bat/sh`** - Scripts de instalación automática
- **`run_app.bat/sh`** - Scripts de ejecución rápida
- **`config.example.py`** - Configuración de ejemplo
- **`requirements.txt`** - Dependencias del proyecto
- **`app/main.py`** - Aplicación principal

### ⚙️ Configuración Necesaria

1. **API Key de OpenAI** (requerida)
   - Edita `config.py` o `.env`
   - Añade tu clave: `OPENAI_API_KEY=tu_clave_aqui`

2. **Variables opcionales**
   - `DEBUG=True/False`
   - `HOST=127.0.0.1`
   - `PORT=8050`

## 🆘 Soporte

Si tienes problemas o preguntas:

1. Revisa la [documentación](docs/)
2. Busca en los [issues existentes](https://github.com/tu-usuario/asistente-medico-inteligente/issues)
3. Crea un nuevo issue si no encuentras la solución

## 🙏 Agradecimientos

- Equipo de la Hackatón Deeppunk 2025
- Comunidad de desarrolladores de IA médica
- Contribuidores y colaboradores del proyecto

---

**Desarrollado con ❤️ para mejorar la atención médica en zonas rurales**
