# 🤖 Asistente Médico Inteligente

**Trabajo presentado para la Hackatón DeeppunkIA 2025**  
Colaboración: Facultad de Ciencias, Universidad Nacional de Colombia, sede Medellín

---

## 🧩 Planteamiento y Motivación

### 🔎 Problemática
En Colombia, millones de personas en zonas rurales enfrentan barreras estructurales, logísticas y económicas para acceder a servicios básicos de salud:
- **Escasez de centros de salud**: En muchos corregimientos o veredas no existe infraestructura médica.
- **Largas distancias y altos costos de transporte**: Llegar a un hospital puede requerir recorrer varios kilómetros a pie o pagar transportes costosos.
- **Falta de médicos especializados**: Incluso si hay un puesto de salud, no suele haber profesionales en medicina general, pediatría, ginecología, etc.
- **Asignación rígida de EPS o médicos**: Muchas veces el médico asignado está lejos, no tiene disponibilidad o el paciente ni lo conoce.
- **Limitado conocimiento médico de la población**: Muchas personas no entienden sus síntomas ni saben si es urgente o tratable en casa.
- **Desconexión tecnológica**: Aunque algunas zonas tienen celular o internet intermitente, no hay soluciones adaptadas a esta realidad.

El resultado: enfermedades tratables se vuelven crónicas o mortales, hay sobrecarga en centros urbanos y pérdida de confianza en el sistema de salud.

---

## 💡 Solución Propuesta

Un **asistente médico inteligente rural**: sistema web ligero y funcional que permite a cualquier persona en una zona rural:
- Describir sus síntomas
- Subir imágenes de radiografías o resultados de laboratorio
- Recibir un diagnóstico preliminar
- Obtener una explicación en lenguaje claro
- Conocer el centro médico más cercano
- Generar un resumen médico para compartir con su médico asignado o el sistema de salud

Este asistente funciona con **agentes inteligentes especializados**, cada uno con una función concreta. Está diseñado para asistir, no reemplazar, y puede operar incluso con conectividad limitada.

---

## 📋 Descripción General

Plataforma web inteligente para diagnóstico preliminar, interpretación de exámenes, análisis de imágenes médicas y apoyo a la toma de decisiones clínicas, especialmente diseñada para zonas rurales o con acceso limitado a especialistas.

Combina procesamiento de lenguaje natural (PLN), visión por computador y agentes inteligentes para asistir a profesionales de la salud y pacientes.

---

## 🏗️ Estructura del Proyecto

```
asistente-medico-inteligente/
│
├── aplicacion.py                # Punto de entrada alternativo, interfaz Dash avanzada
├── app/                        # Frontend Dash: componentes, callbacks, estilos
│   ├── app.py                  # Punto de entrada principal (Dash)
│   ├── components/             # Componentes visuales reutilizables
│   ├── callbacks/              # Lógica de interacción y callbacks Dash
│   ├── styles/                 # Estilos y temas visuales
│   ├── util/                   # Utilidades frontend
│   └── assets/                 # Recursos estáticos (iconos, imágenes)
│
├── agents/                     # Agentes inteligentes (PLN, diagnóstico, orquestación)
│   ├── agente.py               # Agente principal
│   ├── orquestador.py          # Orquestador de agentes
│   ├── diagnostico.py          # Diagnóstico por síntomas
│   ├── exams.py                # Interpretación de exámenes
│   ├── analizarImagenes.py     # Análisis de imágenes médicas
│   ├── contactoMedico.py       # Contacto y asignación de médicos
│   ├── busqueda.py             # Búsqueda de centros médicos
│   ├── explicacion.py          # Explicación de términos médicos
│   └── interpretacionExamenes.py # Interpretación avanzada de exámenes
│
├── vision/                     # Modelos de visión computacional
│   ├── brain_tumor/            # Detección de tumores cerebrales
│   ├── burn/                   # Clasificación de quemaduras
│   ├── chest_x_rays/           # Análisis de rayos X de tórax
│   └── skin_disease/           # Detección de enfermedades de la piel
│
├── prompts/                    # Prompts personalizados para agentes y modelos
│   ├── diagnostico.txt
│   ├── analisis_imagenes.txt
│   ├── interpretacion_examenes.txt
│   ├── explicacion_medica.txt
│   ├── contacto_medico.txt
│   ├── busqueda_centros.txt
│   ├── clasificador.txt
│   └── prototipo.txt
│
├── data/                       # Datos de ejemplo
│   ├── pdfs/                   # Ejemplos de exámenes en PDF
│   └── txt/                    # Ejemplos de resultados en texto
│
├── utils/                      # Utilidades generales
│   ├── conversation.py         # Manejo de conversaciones
│   └── funcionalidades.py      # Funciones auxiliares
│
├── requirements.txt            # Dependencias del proyecto
├── config.example.py           # Configuración de ejemplo
├── env.example                 # Variables de entorno de ejemplo
├── LICENSE                     # Licencia
└── README.md                   # Este archivo
```

---

## 🚀 Instalación

### Instalación Automática (Recomendada)

#### Windows
```bash
git clone https://github.com/tu-usuario/asistente-medico-inteligente.git
cd asistente-medico-inteligente
setup.bat
```

#### Linux / macOS
```bash
git clone https://github.com/tu-usuario/asistente-medico-inteligente.git
cd asistente-medico-inteligente
bash setup.sh
```

### Instalación Manual

1. Clona el repositorio y entra a la carpeta:
   ```bash
   git clone https://github.com/tu-usuario/asistente-medico-inteligente.git
   cd asistente-medico-inteligente
   ```
2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   # Activa el entorno
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Copia y configura las variables de entorno:
   ```bash
   cp env.example .env
   # Edita .env con tus claves y rutas necesarias
   ```

---

## 🏃‍♂️ Uso

1. Activa el entorno virtual si no lo has hecho.
2. Ejecuta la aplicación principal:
   ```bash
   python app/app.py
   ```
3. Abre tu navegador en [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

## ⚙️ Funcionalidades Principales

| Nº | Funcionalidad                                 | Descripción                                                                                 | Estado         |
|----|-----------------------------------------------|---------------------------------------------------------------------------------------------|---------------|
| 1  | Diagnóstico preliminar por texto              | Recibe síntomas y genera diagnóstico posible, urgencia y explicación clara                  | Implementado  |
| 2  | Análisis de imágenes médicas                  | Sube radiografías o fotos de lesiones para análisis automático                              | Implementado  |
| 3  | Interpretación de exámenes (PDF o imagen)     | Lee valores de exámenes clínicos, compara con rangos normales y sugiere observaciones       | Implementado  |
| 4  | Explicación médica en lenguaje claro           | Traduce términos técnicos a lenguaje sencillo                                               | Implementado  |
| 5  | Buscador de centros médicos cercanos           | Muestra centros de salud cercanos según ubicación                                           | Implementado  |
| 6  | Generación de resumen médico para remisión     | Crea reporte con datos del paciente y hallazgos                                             | Implementado  |
| 7  | Simulación de contacto con el médico asignado  | Simula envío del caso al médico o centro más cercano                                        | Parcial       |
| 8  | Agente de ética y advertencia                  | Muestra advertencias y recordatorios éticos al usuario                                      | Implementado  |

> **Nota:** Algunas funcionalidades pueden estar en desarrollo o simuladas según el alcance de la hackatón.

---

## 🧠 Módulos y Agentes

- **Agentes Inteligentes:**
  - Orquestador, diagnóstico, interpretación de exámenes, análisis de imágenes, explicación médica, contacto médico, búsqueda de centros.
- **Modelos de Visión:**
  - Tumores cerebrales, quemaduras, rayos X de tórax, enfermedades de la piel (cada uno con su propio modelo y script de inferencia).
- **Prompts Personalizados:**
  - Prompts para cada tarea de PLN y visión, fácilmente editables en la carpeta `prompts/`.
- **Datos de Ejemplo:**
  - PDFs y archivos de texto en `data/` para pruebas y demostraciones.

---

## 🎯 Valor Diferencial

- No es solo un chatbot: es un ecosistema de agentes colaborativos.
- Integra visión artificial, lenguaje natural, análisis de documentos y contexto local.
- Ofrece acción realista y ética, adaptada a la ruralidad colombiana.
- Escalable y fácilmente integrable con sistemas reales de salud.
- Viable en Python: todo el stack es open source y portable.

---

## ⚠️ Enfoque Ético y Limitaciones

- El sistema **no reemplaza** la consulta médica profesional.
- Siempre se muestran advertencias y recordatorios éticos.
- El diagnóstico es preliminar y orientativo.
- Se promueve la consulta con profesionales de la salud ante cualquier duda o urgencia.

---

## 📦 Dependencias Principales

- dash, dash-bootstrap-components, plotly, pandas
- langchain, langchain-community
- opencv-python, Pillow
- python-dotenv, tqdm, requests
- llama-cpp-python, transformers, PyMuPDF
- ultralytics, tensorflow

(Ver `requirements.txt` para la lista completa y versiones)

---

## 👥 Créditos y Colaboradores

- **Equipo de desarrollo:** Participantes Hackatón DeeppunkIA 2025
- **Colaboración académica:** Facultad de Ciencias, Universidad Nacional de Colombia, sede Medellín

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

---

## 📬 Contacto y Contribución

¿Quieres contribuir o tienes dudas? ¡Bienvenido! Puedes abrir issues o pull requests en el repositorio, o contactar al equipo organizador de la Hackatón DeeppunkIA.
