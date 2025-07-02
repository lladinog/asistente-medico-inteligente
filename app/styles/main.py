"""
Estilos principales de la aplicación
Centraliza todos los estilos CSS para evitar repetición
"""

# Estilos del layout principal
MAIN_STYLES = {
    'main-container': {
        'backgroundColor': '#0f0f17',
        'color': '#ffffff',
        'height': '100vh',
        'display': 'flex',
        'flexDirection': 'row',
        'overflow': 'hidden',
        'position': 'relative'
    },
    'floating-sidebar-toggle': {
        'position': 'fixed',
        'left': '10px',
        'top': '10px',
        'backgroundColor': '#6a0dad',
        'border': 'none',
        'color': 'white',
        'borderRadius': '5px',
        'width': '30px',
        'height': '30px',
        'cursor': 'pointer',
        'zIndex': 1000,
        'display': 'none',
        'alignItems': 'center',
        'justifyContent': 'center'
    }
}

# Colores del tema
THEME_COLORS = {
    'primary': '#6a0dad',
    'secondary': '#b19cd9',
    'accent': '#d3bcf6',
    'background': '#0f0f17',
    'surface': '#1a1a3a',
    'surface_secondary': '#2a2a4a',
    'surface_tertiary': '#3a3a5a',
    'functional_bg': '#151525',
    'border': '#444',
    'text_primary': '#ffffff',
    'text_secondary': '#b19cd9',
    'text_muted': '#888'
}

# Transiciones
TRANSITIONS = {
    'default': 'all 0.3s ease',
    'fast': 'all 0.2s ease',
    'slow': 'all 0.5s ease'
}

# Sombras
SHADOWS = {
    'small': '0 1px 2px rgba(0,0,0,0.1)',
    'medium': '0 2px 4px rgba(0,0,0,0.1)',
    'large': '0 4px 8px rgba(0,0,0,0.2)'
}

# Bordes redondeados
BORDER_RADIUS = {
    'small': '5px',
    'medium': '10px',
    'large': '18px',
    'circle': '50%'
} 