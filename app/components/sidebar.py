import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from styles.sidebar import SIDEBAR_STYLES

def create_sidebar_component():
    """Crea el componente Sidebar"""
    
    return html.Div([
        html.Div([
            dbc.Button(
                html.I(className="fas fa-times"),
                id='sidebar-toggle',
                style={**SIDEBAR_STYLES['sidebar-toggle'], 'position': 'absolute', 'left': '15px', 'top': '15px', 'right': 'unset'}
            )
        ], style={'position': 'relative', 'height': '40px', 'marginBottom': '10px'}),
        dbc.Button(
            [html.I(className="fas fa-plus", style={'marginRight': '8px'}), "Nueva conversación"],
            id='new-chat-button',
            style=SIDEBAR_STYLES['new-chat-button']
        ),
        html.Div(id='conversations-list', children=[])
    ], id='sidebar', style=SIDEBAR_STYLES['sidebar'])

# Los callbacks se manejan en el archivo principal app_refactored.py 