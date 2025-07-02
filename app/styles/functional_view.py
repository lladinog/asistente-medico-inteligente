"""
Estilos específicos para el componente FunctionalView
"""

from .main import THEME_COLORS, TRANSITIONS, BORDER_RADIUS, SHADOWS

FUNCTIONAL_VIEW_STYLES = {
    'functional-view': {
        'width': '400px',
        'backgroundColor': THEME_COLORS['functional_bg'],
        'borderLeft': f'1px solid {THEME_COLORS["border"]}',
        'overflowY': 'auto',
        'padding': '20px',
        'flexShrink': 0,
        'transition': TRANSITIONS['default'],
        'display': 'flex',
        'flexDirection': 'column',
        'minWidth': 0
    },
    'functional-view-hidden': {
        'width': '0',
        'padding': '0',
        'borderLeft': 'none',
        'overflow': 'hidden'
    },
    'functional-close-button': {
        'position': 'absolute',
        'left': '-40px',
        'top': '10px',
        'backgroundColor': THEME_COLORS['primary'],
        'border': 'none',
        'color': THEME_COLORS['text_primary'],
        'borderRadius': BORDER_RADIUS['small'],
        'width': '30px',
        'height': '30px',
        'cursor': 'pointer',
        'zIndex': 101,
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'transition': TRANSITIONS['fast']
    },
    'functional-close-button:hover': {
        'backgroundColor': THEME_COLORS['secondary']
    },
    'functional-header': {
        'color': THEME_COLORS['text_secondary'],
        'marginBottom': '20px',
        'paddingBottom': '10px',
        'borderBottom': f'1px solid {THEME_COLORS["border"]}'
    },
    'functional-content': {
        'flexGrow': 1,
        'color': THEME_COLORS['text_primary']
    },
    'content-card': {
        'backgroundColor': THEME_COLORS['surface_secondary'],
        'border': 'none',
        'marginBottom': '15px',
        'borderRadius': BORDER_RADIUS['medium'],
        'boxShadow': SHADOWS['small']
    },
    'content-card-header': {
        'color': THEME_COLORS['text_secondary'],
        'fontWeight': 'bold',
        'marginBottom': '10px'
    },
    'content-list': {
        'margin': '0',
        'paddingLeft': '20px'
    },
    'content-list-item': {
        'marginBottom': '5px',
        'color': THEME_COLORS['text_primary']
    },
    'content-text': {
        'color': THEME_COLORS['text_primary'],
        'lineHeight': '1.6'
    },
    'content-strong': {
        'color': THEME_COLORS['text_secondary'],
        'fontWeight': 'bold'
    }
} 