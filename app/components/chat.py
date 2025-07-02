import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

def create_chat_component():
    """Crea el componente Chat"""
    
    styles = {
        'chat-container': {
            'flex': 1,
            'display': 'flex',
            'flexDirection': 'column',
            'height': '100vh',
            'transition': 'all 0.3s ease',
            'position': 'relative',
            'minWidth': 0  # Permite que el flex se encoja
        },
        'chat-header': {
            'backgroundColor': '#1a1a3a',
            'color': 'white',
            'padding': '15px',
            'borderBottom': '1px solid #444',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'space-between',
            'flexShrink': 0
        },
        'chat-messages': {
            'flexGrow': 1,
            'overflowY': 'auto',
            'padding': '20px',
            'background': '#0f0f17',
            'display': 'flex',
            'flexDirection': 'column',
            'minHeight': 0  # Permite que el flex se encoja
        },
        'message-input-container': {
            'padding': '15px',
            'backgroundColor': '#1a1a3a',
            'borderTop': '1px solid #444',
            'position': 'relative',
            'flexShrink': 0
        },
        'user-message': {
            'backgroundColor': '#6a0dad',
            'color': 'white',
            'padding': '12px 16px',
            'borderRadius': '18px 18px 4px 18px',
            'marginBottom': '10px',
            'maxWidth': '80%',
            'alignSelf': 'flex-end',
            'boxShadow': '0 1px 2px rgba(0,0,0,0.1)',
            'wordWrap': 'break-word'
        },
        'bot-message': {
            'backgroundColor': '#2a2a4a',
            'color': 'white',
            'padding': '12px 16px',
            'borderRadius': '18px 18px 18px 4px',
            'marginBottom': '10px',
            'maxWidth': '80%',
            'alignSelf': 'flex-start',
            'boxShadow': '0 1px 2px rgba(0,0,0,0.1)',
            'wordWrap': 'break-word'
        },
        'input-textarea': {
            'width': '100%',
            'backgroundColor': '#2a2a4a',
            'color': 'white',
            'border': 'none',
            'borderRadius': '20px',
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
            'backgroundColor': '#6a0dad',
            'border': 'none',
            'color': 'white',
            'borderRadius': '50%',
            'width': '40px',
            'height': '40px',
            'cursor': 'pointer',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center'
        }
    }
    
    return html.Div([
        # Encabezado del chat
        html.Div(style=styles['chat-header'], children=[
            dbc.Button(
                html.I(className="fas fa-bars"),
                id='mobile-sidebar-toggle',
                style={'backgroundColor': 'transparent', 'border': 'none', 'color': 'white'}
            ),
            html.Div("Asistente Médico Rural", style={'fontWeight': 'bold', 'flexGrow': 1, 'textAlign': 'center'}),
            dbc.ButtonGroup([
                dbc.Button(
                    html.I(className="fas fa-diagnoses"),
                    id='diagnostico-button',
                    color="link",
                    style={'color': '#d3bcf6'}
                ),
                dbc.Button(
                    html.I(className="fas fa-book-medical"),
                    id='explicacion-button',
                    color="link",
                    style={'color': '#d3bcf6'}
                )
            ])
        ]),
        
        # Mensajes del chat
        html.Div(id='chat-messages', style=styles['chat-messages'], children=[
            html.Div(style={'textAlign': 'center', 'padding': '20px', 'color': '#b19cd9'}, children=[
                html.H5("Bienvenido al Asistente Médico Rural"),
                html.P("Soy tu asistente de salud virtual. ¿En qué puedo ayudarte hoy?"),
                html.P("Puedes preguntarme sobre síntomas, diagnósticos o explicaciones médicas.")
            ])
        ]),
        
        # Entrada de mensajes
        html.Div(style=styles['message-input-container'], children=[
            dbc.InputGroup(children=[
                dbc.Textarea(
                    id='user-input',
                    placeholder="Escribe tu consulta médica...",
                    style=styles['input-textarea'],
                    rows=1
                ),
                dbc.Button(
                    html.I(className="fas fa-paper-plane"),
                    id='send-button',
                    style=styles['send-button']
                )
            ])
        ])
    ], id='chat-container', style=styles['chat-container']) 