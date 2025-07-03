"""
Estilos específicos para el componente Chat
"""

from .main import THEME_COLORS, TRANSITIONS, BORDER_RADIUS, SHADOWS

CHAT_STYLES = {
    'chat-container': {
        'flex': 1,
        'display': 'flex',
        'flexDirection': 'column',
        'height': '100%',
        'width': '100%',
        'transition': TRANSITIONS['default'],
        'position': 'relative',
        'minWidth': 0,
        'minHeight': 0
    },
    'chat-header': {
        'backgroundColor': THEME_COLORS['surface'],
        'color': THEME_COLORS['text_primary'],
        'padding': '15px',
        'borderBottom': f'1px solid {THEME_COLORS["border"]}',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'space-between',
        'flexShrink': 0
    },
    'chat-messages': {
        'flexGrow': 1,
        'overflowY': 'auto',
        'padding': '20px',
        'background': THEME_COLORS['background'],
        'display': 'flex',
        'flexDirection': 'column',
        'minHeight': 0  # Permite que el flex se encoja
    },
    'message-input-container': {
        'padding': '15px',
        'backgroundColor': THEME_COLORS['surface'],
        'borderTop': f'1px solid {THEME_COLORS["border"]}',
        'position': 'relative',
        'flexShrink': 0
    },
    'user-message': {
        'backgroundColor': THEME_COLORS['primary'],
        'color': THEME_COLORS['text_primary'],
        'padding': '12px 16px',
        'borderRadius': f'{BORDER_RADIUS["large"]} {BORDER_RADIUS["large"]} 4px {BORDER_RADIUS["large"]}',
        'marginBottom': '10px',
        'maxWidth': '80%',
        'alignSelf': 'flex-end',
        'boxShadow': SHADOWS['small'],
        'wordWrap': 'break-word'
    },
    'bot-message': {
        'backgroundColor': THEME_COLORS['surface_secondary'],
        'color': THEME_COLORS['text_primary'],
        'padding': '12px 16px',
        'borderRadius': f'{BORDER_RADIUS["large"]} {BORDER_RADIUS["large"]} {BORDER_RADIUS["large"]} 4px',
        'marginBottom': '10px',
        'maxWidth': '80%',
        'alignSelf': 'flex-start',
        'boxShadow': SHADOWS['small'],
        'wordWrap': 'break-word'
    },
    'input-textarea': {
        'width': '100%',
        'backgroundColor': THEME_COLORS['surface_secondary'],
        'color': THEME_COLORS['text_primary'],
        'border': 'none',
        'borderRadius': BORDER_RADIUS['large'],
        'padding': '12px 20px',
        'resize': 'none',
        'minHeight': '50px',
        'maxHeight': '150px',
        'paddingRight': '50px'
    },
    'send-button': {
        'position': 'absolute',
        'right': '25px',
        'bottom': '25px',
        'backgroundColor': THEME_COLORS['primary'],
        'border': 'none',
        'color': THEME_COLORS['text_primary'],
        'borderRadius': BORDER_RADIUS['circle'],
        'width': '40px',
        'height': '40px',
        'cursor': 'pointer',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'transition': TRANSITIONS['fast'],
        'zIndex': 10
    },
    'send-button:hover': {
        'backgroundColor': THEME_COLORS['secondary']
    },
    'welcome-message': {
        'textAlign': 'center',
        'padding': '20px',
        'color': THEME_COLORS['text_secondary'],
        'fontStyle': 'italic'
    },
    'header-button': {
        'backgroundColor': 'transparent',
        'border': 'none',
        'color': THEME_COLORS['text_primary'],
        'cursor': 'pointer',
        'transition': TRANSITIONS['fast']
    },
    'header-button:hover': {
        'color': THEME_COLORS['accent']
    },
    'header-button-group': {
        'display': 'flex',
        'gap': '10px'
    }
} 