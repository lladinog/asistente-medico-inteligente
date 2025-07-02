import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

def create_sidebar_component():
    """Crea el componente Sidebar"""
    
    styles = {
        'sidebar': {
            'width': '300px',
            'backgroundColor': '#1a1a3a',
            'padding': '15px',
            'borderRight': '1px solid #444',
            'transition': 'all 0.3s ease',
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
            'backgroundColor': '#6a0dad',
            'border': 'none',
            'color': 'white',
            'borderRadius': '5px',
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
            'borderRadius': '5px',
            'cursor': 'pointer',
            'backgroundColor': '#2a2a4a',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'whiteSpace': 'nowrap',
            'transition': 'all 0.2s ease'
        },
        'new-chat-button': {
            'width': '100%',
            'marginBottom': '15px',
            'backgroundColor': '#6a0dad',
            'border': 'none',
            'color': 'white',
            'padding': '10px',
            'borderRadius': '5px',
            'cursor': 'pointer',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center'
        }
    }
    
    return html.Div([
        dbc.Button(
            html.I(className="fas fa-times"),
            id='sidebar-toggle',
            style=styles['sidebar-toggle']
        ),
        dbc.Button(
            [html.I(className="fas fa-plus", style={'marginRight': '8px'}), "Nueva conversación"],
            id='new-chat-button',
            style=styles['new-chat-button']
        ),
        html.Div(id='conversations-list', children=[])
    ], id='sidebar', style=styles['sidebar'])

# Los callbacks se manejan en el archivo principal app_refactored.py 