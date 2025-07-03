# Estructura Modular - Health IA

## 🏗️ Arquitectura Modular

La aplicación ahora está completamente modularizada con una estructura limpia y organizada:

```
app/
├── components/           # Componentes de la interfaz
│   ├── __init__.py
│   ├── sidebar.py       # Componente del sidebar
│   ├── chat.py          # Componente del chat
│   └── functional_view.py # Componente de vista funcional
├── styles/              # Estilos centralizados
│   ├── __init__.py
│   ├── main.py          # Estilos principales y tema
│   ├── sidebar.py       # Estilos del sidebar
│   ├── chat.py          # Estilos del chat
│   └── functional_view.py # Estilos de vista funcional
├── callbacks/           # Callbacks organizados
│   ├── __init__.py
│   ├── sidebar.py       # Callbacks del sidebar
│   ├── chat.py          # Callbacks del chat
│   └── navigation.py    # Callbacks de navegación
├── utils/               # Utilidades comunes
│   ├── __init__.py
│   └── helpers.py       # Funciones de utilidad
└── app.py       # Aplicación completamente modular
```

## 🎨 Sistema de Estilos Centralizado

### **Tema de Colores**
```python
THEME_COLORS = {
    'primary': '#6a0dad',      # Color principal
    'secondary': '#b19cd9',    # Color secundario
    'accent': '#d3bcf6',       # Color de acento
    'background': '#0f0f17',   # Fondo principal
    'surface': '#1a1a3a',      # Superficies
    'surface_secondary': '#2a2a4a',
    'surface_tertiary': '#3a3a5a',
    'functional_bg': '#151525',
    'border': '#444',
    'text_primary': '#ffffff',
    'text_secondary': '#b19cd9',
    'text_muted': '#888'
}
```

### **Transiciones y Efectos**
```python
TRANSITIONS = {
    'default': 'all 0.3s ease',
    'fast': 'all 0.2s ease',
    'slow': 'all 0.5s ease'
}

SHADOWS = {
    'small': '0 1px 2px rgba(0,0,0,0.1)',
    'medium': '0 2px 4px rgba(0,0,0,0.1)',
    'large': '0 4px 8px rgba(0,0,0,0.2)'
}
```

## 🔧 Componentes Modulares

### **1. Sidebar Component**
```python
from components.sidebar import create_sidebar_component

# Crea el sidebar con estilos centralizados
sidebar = create_sidebar_component()
```

**Características:**
- Lista de conversaciones
- Botón de nueva conversación
- Toggle para mostrar/ocultar
- Estilos responsivos

### **2. Chat Component**
```python
from components.chat import create_chat_component

# Crea el chat con estilos centralizados
chat = create_chat_component()
```

**Características:**
- Mensajes del usuario y bot
- Entrada de texto
- Botones de funcionalidad
- Layout responsive

### **3. Functional View Component**
```python
from components.functional_view import create_functional_view_component

# Crea la vista funcional
functional_view = create_functional_view_component()
```

**Características:**
- Contenido dinámico
- Botón de cerrar
- Ancho fijo responsive

## 📞 Callbacks Organizados

### **1. Sidebar Callbacks**
```python
from callbacks.sidebar import register_sidebar_callbacks

# Registra callbacks del sidebar
register_sidebar_callbacks(app)
```

**Funciones:**
- `toggle_sidebar()` - Mostrar/ocultar sidebar
- `update_conversations_list()` - Actualizar lista de conversaciones

### **2. Chat Callbacks**
```python
from callbacks.chat import register_chat_callbacks

# Registra callbacks del chat
register_chat_callbacks(app, orquestador)
```

**Funciones:**
- `update_chat()` - Manejar mensajes del chat
- Integración con el orquestador

### **3. Navigation Callbacks**
```python
from callbacks.navigation import register_navigation_callbacks

# Registra callbacks de navegación
register_navigation_callbacks(app)
```

**Funciones:**
- `update_functional_view()` - Manejar vista funcional
- `navigate_to_functionality()` - Navegación entre páginas

## 🛠️ Utilidades Comunes

### **Funciones de Ayuda**
```python
from utils.helpers import (
    generate_session_id,
    truncate_text,
    create_conversation_item,
    merge_styles,
    validate_input,
    sanitize_text
)
```

**Funciones disponibles:**
- `generate_session_id()` - Generar ID único de sesión
- `truncate_text()` - Truncar texto largo
- `create_conversation_item()` - Crear elemento de conversación
- `merge_styles()` - Combinar estilos
- `validate_input()` - Validar entrada de usuario
- `sanitize_text()` - Sanitizar texto

## 🚀 Cómo Usar

### **Para desarrollo:**
```bash
# Usar la aplicación modular
python app/app_modular.py
```

### **Para producción:**
```bash
# Usar la aplicación original
python app/app.py
```

## ✨ Ventajas de la Estructura Modular

### **1. Mantenibilidad**
- Cada componente tiene su propia lógica
- Fácil encontrar y modificar código
- Separación clara de responsabilidades

### **2. Reutilización**
- Componentes se pueden reutilizar
- Estilos centralizados evitan duplicación
- Funciones de utilidad compartidas

### **3. Escalabilidad**
- Fácil agregar nuevos componentes
- Estructura preparada para crecimiento
- Patrones consistentes

### **4. Responsive Design**
- Chat siempre ocupa espacio disponible
- Componentes se ajustan automáticamente
- Transiciones suaves

### **5. Organización**
- Código bien estructurado
- Fácil navegación entre archivos
- Documentación clara

## 🔄 Flujo de Datos

```
Usuario → Componente → Callback → Orquestador → Respuesta → UI
```

1. **Usuario interactúa** con un componente
2. **Callback se ejecuta** y procesa la interacción
3. **Orquestador procesa** la lógica de negocio
4. **Respuesta se envía** de vuelta al UI
5. **Componente se actualiza** con la nueva información

## 📝 Próximos Pasos

1. **Agregar más funcionalidades** como componentes separados
2. **Implementar tests** para cada componente
3. **Optimizar rendimiento** con lazy loading
4. **Agregar más utilidades** según necesidades
5. **Crear documentación** más detallada

## 🎯 Beneficios Logrados

- ✅ **Código más limpio** y organizado
- ✅ **Estilos centralizados** sin duplicación
- ✅ **Componentes reutilizables**
- ✅ **Callbacks organizados** por funcionalidad
- ✅ **Funciones de utilidad** compartidas
- ✅ **Layout responsive** mejorado
- ✅ **Mantenimiento más fácil**
- ✅ **Escalabilidad mejorada** 