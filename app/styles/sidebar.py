"""
Estilos específicos para el componente Sidebar
"""

from .main import THEME_COLORS, TRANSITIONS, BORDER_RADIUS

SIDEBAR_STYLES = {
    'sidebar': {
        'width': '300px',
        'backgroundColor': THEME_COLORS['surface'],
        'padding': '15px',
        'borderRight': f'1px solid {THEME_COLORS["border"]}',
        'transition': TRANSITIONS['default'],
        'overflowY': 'auto',
        'height': '100vh',
        'position': 'relative',
        'zIndex': 10,
        'flexShrink': 0
    },
    'sidebar-hidden': {
        'transform': 'translateX(-100%)',
        'width': '0',
        'padding': '0',
        'borderRight': 'none'
    },
    'sidebar-toggle': {
        'position': 'absolute',
        'right': '-40px',
        'top': '10px',
        'backgroundColor': THEME_COLORS['primary'],
        'border': 'none',
        'color': THEME_COLORS['text_primary'],
        'borderRadius': BORDER_RADIUS['small'],
        'width': '30px',
        'height': '30px',
        'cursor': 'pointer',
        'zIndex': 1000,
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center'
    },
    'conversation-item': {
        'padding': '10px',
        'marginBottom': '5px',
        'borderRadius': BORDER_RADIUS['small'],
        'cursor': 'pointer',
        'backgroundColor': THEME_COLORS['surface_secondary'],
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'whiteSpace': 'nowrap',
        'transition': TRANSITIONS['fast'],
        'color': THEME_COLORS['text_primary']
    },
    'conversation-item:hover': {
        'backgroundColor': THEME_COLORS['surface_tertiary']
    },
    'conversation-item-active': {
        'backgroundColor': THEME_COLORS['primary']
    },
    'new-chat-button': {
        'width': '100%',
        'marginBottom': '15px',
        'backgroundColor': THEME_COLORS['primary'],
        'border': 'none',
        'color': THEME_COLORS['text_primary'],
        'padding': '10px',
        'borderRadius': BORDER_RADIUS['small'],
        'cursor': 'pointer',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'transition': TRANSITIONS['fast']
    },
    'new-chat-button:hover': {
        'backgroundColor': THEME_COLORS['secondary']
    }
} 