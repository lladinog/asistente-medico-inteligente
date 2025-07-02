import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from styles.chat import CHAT_STYLES
from utils.funcionalidades import FuncionalidadMedica

def create_funcionalidades_menu():
    """Genera el menú de funcionalidades desde el Enum"""
    items = []
    for idx, funcionalidad in enumerate(FuncionalidadMedica, 1):
        items.append(
            html.Li(f"{idx}. {funcionalidad.emoji} {funcionalidad.label}  ({funcionalidad.key})", style={'marginBottom': '6px'})
        )
    return html.Ul(items, style={'textAlign': 'left', 'color': '#b19cd9'})

def create_chat_component():
    """Crea el componente Chat"""

    return html.Div([
        # Encabezado del chat
        html.Div(style=CHAT_STYLES['chat-header'], children=[
            html.Div("Asistente Médico Rural", style={'fontWeight': 'bold', 'flexGrow': 1, 'textAlign': 'center'}),
            dbc.ButtonGroup([
                dbc.Button(
                    html.I(className="fas fa-diagnoses"),
                    id='diagnostico-button',
                    color="link",
                    style={'color': '#d3bcf6'},
                    title="Diagnóstico"
                ),
                dbc.Button(
                    html.I(className="fas fa-book-medical"),
                    id='explicacion-button',
                    color="link",
                    style={'color': '#d3bcf6'},
                    title="Explicación Médica"
                ),
                dbc.Button(
                    html.I(className="fas fa-microscope"),
                    id='interpretacion-examenes-button',
                    color="link",
                    style={'color': '#d3bcf6'},
                    title="Interpretación de Exámenes"
                ),
                dbc.Button(
                    html.I(className="fas fa-file-medical"),
                    id='resumen-medico-button',
                    color="link",
                    style={'color': '#d3bcf6'},
                    title="Resumen Médico"
                ),
                dbc.Button(
                    html.I(className="fas fa-user-md"),
                    id='contacto-medico-button',
                    color="link",
                    style={'color': '#d3bcf6'},
                    title="Contacto Médico"
                ),
                dbc.Button(
                    html.I(className="fas fa-search"),
                    id='busqueda-button',
                    color="link",
                    style={'color': '#d3bcf6'},
                    title="Búsqueda Médica"
                ),
                dbc.Button(
                    html.I(className="fas fa-image"),
                    id='analizar-imagenes-button',
                    color="link",
                    style={'color': '#d3bcf6'},
                    title="Análisis de Imágenes"
                )
            ])
        ]),

        # Mensajes del chat
        html.Div(id='chat-messages', style=CHAT_STYLES['chat-messages'], children=[
            html.Div(style=CHAT_STYLES['welcome-message'], children=[
                html.H5("Bienvenido al Asistente Médico Rural"),
                html.P("Soy tu asistente de salud virtual. ¿En qué puedo ayudarte hoy?"),
                html.P("Puedes escribir el número o el nombre exacto de la funcionalidad para acceder directamente."),
                html.Br(),
                html.Div(style={'textAlign': 'left', 'marginTop': '20px'}, children=[
                    html.H6("Menú de funcionalidades:", style={'color': '#b19cd9', 'marginBottom': '10px'}),
                    create_funcionalidades_menu()
                ])
            ])
        ]),

        # Input del usuario
        html.Div(style=CHAT_STYLES['message-input-container'], children=[
            dbc.InputGroup(children=[
                dbc.Textarea(
                    id='user-input',
                    placeholder="Escribe tu consulta médica, número o nombre de funcionalidad...",
                    rows=1,
                    style=CHAT_STYLES['input-textarea']
                ),
                dbc.Button(
                    html.I(className="fas fa-paper-plane"),
                    id='send-button',
                    style=CHAT_STYLES['send-button']
                )
            ])
        ])
    ], id='chat-container', style=CHAT_STYLES['chat-container'])