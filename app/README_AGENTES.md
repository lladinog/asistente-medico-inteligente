# Páginas de Agentes - Health IA

## 🎯 Elemento Functional View

El elemento que aparece a la mitad del chat es el **Functional View** (vista funcional), que se muestra cuando se activa una funcionalidad específica de un agente. Este componente:

- **Aparece a la derecha** del chat cuando se activa un agente
- **Tiene un ancho fijo** de 400px
- **Se puede cerrar** con el botón X
- **Muestra contenido específico** para cada agente
- **Es responsive** y se ajusta al layout

## 🤖 Agentes Disponibles

### **1. 🔍 Agente de Diagnóstico**
- **Archivo**: `agents/diagnostico.py`
- **Ruta**: `/diagnostico`
- **Botón**: 🔍 (fas fa-diagnoses)
- **Funcionalidad**: Análisis de síntomas y posibles diagnósticos

**Página incluye:**
- 📋 Síntomas analizados
- 🏥 Posibles diagnósticos
- ⚠️ Recomendaciones médicas

### **2. 📚 Agente de Explicación Médica**
- **Archivo**: `agents/explicacion.py`
- **Ruta**: `/explicacion`
- **Botón**: 📚 (fas fa-book-medical)
- **Funcionalidad**: Explicación de términos y conceptos médicos

**Página incluye:**
- 🔤 Términos explicados
- 📖 Conceptos médicos

### **3. 🔬 Agente de Interpretación de Exámenes**
- **Archivo**: `agents/interpretacionExamenes.py`
- **Ruta**: `/interpretacion-examenes`
- **Botón**: 🔬 (fas fa-microscope)
- **Funcionalidad**: Análisis e interpretación de resultados de exámenes

**Página incluye:**
- 📊 Resultados de exámenes
- 📈 Valores de referencia
- ⚠️ Información importante

### **4. 📋 Agente de Resumen Médico**
- **Archivo**: `agents/resumenMedico.py`
- **Ruta**: `/resumen-medico`
- **Botón**: 📋 (fas fa-file-medical)
- **Funcionalidad**: Generación de resúmenes médicos

**Página incluye:**
- 📝 Información del paciente
- 📄 Resumen generado

### **5. 👨‍⚕️ Agente de Contacto Médico**
- **Archivo**: `agents/contactoMedico.py`
- **Ruta**: `/contacto-medico`
- **Botón**: 👨‍⚕️ (fas fa-user-md)
- **Funcionalidad**: Información de contacto de profesionales

**Página incluye:**
- 🏥 Centros médicos cercanos
- 👨‍⚕️ Especialistas
- 📞 Información de contacto

### **6. 🔍 Agente de Búsqueda**
- **Archivo**: `agents/busqueda.py`
- **Ruta**: `/busqueda`
- **Botón**: 🔍 (fas fa-search)
- **Funcionalidad**: Búsqueda de información médica

**Página incluye:**
- 📚 Recursos médicos
- 📖 Artículos y estudios

### **7. 🖼️ Agente de Análisis de Imágenes**
- **Archivo**: `agents/analizarImagenes.py`
- **Ruta**: `/analizar-imagenes`
- **Botón**: 🖼️ (fas fa-image)
- **Funcionalidad**: Análisis de imágenes médicas

**Página incluye:**
- 📸 Imagen analizada
- 🔍 Resultados del análisis
- ⚠️ Limitaciones

## 🎨 Diseño de las Páginas

### **Estructura Común**
Cada página sigue la misma estructura:

```python
def create_[agente]_content():
    return html.Div([
        html.H4("🎯 Título del Agente", style=STYLES['header']),
        html.P("Descripción de la funcionalidad", style=STYLES['text']),
        
        # Tarjetas de contenido específico
        dbc.Card([...]),
        dbc.Card([...]),
        dbc.Card([...])
    ])
```

### **Elementos de Diseño**
- **Iconos emoji** para identificación visual
- **Tarjetas organizadas** para cada sección
- **IDs únicos** para actualización dinámica
- **Estilos consistentes** del tema

## 🔄 Flujo de Interacción

### **1. Activación del Agente**
```
Usuario hace clic en botón → Se activa agente → Se muestra página específica
```

### **2. Navegación**
```
Chat → Botón del agente → Functional View → Página específica
```

### **3. Cierre**
```
Botón X → Se oculta Functional View → Chat ocupa todo el espacio
```

## 📱 Responsive Design

### **Comportamiento del Layout**
- **Solo Chat**: Ocupa 100% del espacio
- **Chat + Sidebar**: Chat se ajusta al espacio restante
- **Chat + Functional View**: Chat se ajusta al espacio restante
- **Los tres**: Chat se ajusta al espacio entre sidebar y functional view

### **Anchos de Componentes**
- **Sidebar**: 300px (fijo)
- **Functional View**: 400px (fijo)
- **Chat**: Flexible (ocupa espacio disponible)

## 🛠️ Implementación Técnica

### **Componentes Involucrados**
1. **`functional_view.py`**: Define las páginas de cada agente
2. **`chat.py`**: Incluye botones para todos los agentes
3. **`navigation.py`**: Maneja la navegación entre páginas
4. **`chat.py` (callbacks)**: Procesa la activación de agentes

### **Callbacks Principales**
```python
# Navegación
@app.callback(Output('url', 'pathname'), Inputs=[...])
def navigate_to_functionality(...)

# Actualización de vista funcional
@app.callback(Output('functional-view', 'style'), Output('functional-content', 'children'), Inputs=[...])
def update_functional_view(...)
```

## 🎯 Beneficios de la Implementación

### **1. Modularidad**
- Cada agente tiene su propia página
- Fácil agregar nuevos agentes
- Contenido específico y relevante

### **2. Experiencia de Usuario**
- Navegación intuitiva con iconos
- Información organizada en tarjetas
- Transiciones suaves

### **3. Mantenibilidad**
- Código organizado por funcionalidad
- Estilos centralizados
- Fácil modificación de páginas

### **4. Escalabilidad**
- Estructura preparada para nuevos agentes
- Patrón consistente de implementación
- Reutilización de componentes

## 🚀 Cómo Usar

### **Para desarrollo:**
```bash
python app/app_modular.py
```

### **Para agregar un nuevo agente:**
1. Crear el agente en `agents/`
2. Agregar función de contenido en `functional_view.py`
3. Agregar botón en `chat.py`
4. Actualizar callbacks en `navigation.py`
5. Registrar agente en `app_modular.py`

## 📝 Próximos Pasos

1. **Implementar actualización dinámica** del contenido de las páginas
2. **Agregar más interactividad** en las páginas
3. **Implementar persistencia** de datos de sesión
4. **Agregar animaciones** de transición
5. **Optimizar rendimiento** con lazy loading 