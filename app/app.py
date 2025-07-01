import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from agents.orquestador import Orquestador, FuncionalidadMedica
from agents.diagnostico import AgenteDiagnostico
from agents.explicacion import AgenteExplicacionMedica

# Configuración inicial
config = {
    "nombre_app": "Asistente Médico Rural",
    "estilo": dbc.themes.BOOTSTRAP
}

model_config = {
    "model_path": "modelos/llama-medical.bin",
    "n_ctx": 2048,
    "n_threads": 8
}

# Inicializar orquestador
orquestador = Orquestador(config, model_config)

# Registrar agentes (ejemplo con algunos)
orquestador.registrar_agente(
    FuncionalidadMedica.DIAGNOSTICO,
    AgenteDiagnostico()
)
orquestador.registrar_agente(
    FuncionalidadMedica.EXPLICACION_MEDICA,
    AgenteExplicacionMedica()
)
# Registrar los demás agentes...

# Crear aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[config["estilo"]])
app.title = config["nombre_app"]

# Layout principal
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-id', storage_type='session'),
    
    # Header
    dbc.NavbarSimple(
        brand="Asistente Médico Rural",
        color="primary",
        dark=True,
        id="navbar"
    ),
    
    # Cuerpo dividido en sidebar y contenido
    dbc.Row([
        # Sidebar con el chat (siempre visible)
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Chat de Consulta"),
                dbc.CardBody([
                    html.Div(id='chat-messages', style={'height': '400px', 'overflowY': 'scroll'}),
                    dbc.InputGroup([
                        dbc.Input(id='user-input', placeholder="Escribe tu consulta...", type="text"),
                        dbc.Button("Enviar", id='send-button', color="primary")
                    ])
                ])
            ]),
            md=4
        ),
        
        # Contenido principal (cambia según la funcionalidad)
        dbc.Col(
            html.Div(id='page-content'),
            md=8
        )
    ])
], fluid=True)

# Páginas de cada funcionalidad
def render_home():
    return html.Div([
        html.H3("Bienvenido al Asistente Médico Rural"),
        html.P("Selecciona una funcionalidad o escribe tu consulta en el chat.")
    ])

def render_diagnostico():
    return html.Div([
        html.H3("Diagnóstico Preliminar"),
        html.P("Aquí puedes describir tus síntomas para recibir un diagnóstico inicial.")
    ])

def render_explicacion():
    return html.Div([
        html.H3("Explicaciones Médicas"),
        html.P("Pregunta sobre cualquier término médico para obtener una explicación sencilla.")
    ])

# Añadir más funciones render_* para cada funcionalidad...

# Callback para cambiar páginas
@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/':
        return render_home()
    elif pathname == '/diagnostico':
        return render_diagnostico()
    elif pathname == '/explicacion':
        return render_explicacion()
    # Añadir más condiciones para cada funcionalidad...
    return render_home()

# Callback para manejar el chat
@callback(
    [Output('chat-messages', 'children'),
     Output('user-input', 'value')],
    [Input('send-button', 'n_clicks'),
     Input('user-input', 'n_submit')],
    [State('user-input', 'value'),
     State('session-id', 'data'),
     State('chat-messages', 'children')]
)
def update_chat(n_clicks, n_submit, user_input, session_id, existing_messages):
    if not user_input or (n_clicks is None and n_submit is None):
        return existing_messages or [], ""
    
    # Obtener o crear session_id
    if not session_id:
        session_id = orquestador._generar_session_id()
    
    # Procesar mensaje con el orquestador
    respuesta = orquestador.procesar_mensaje(session_id, user_input)
    
    # Actualizar mensajes del chat
    new_messages = (existing_messages or []) + [
        html.P(f"Usuario: {user_input}", className="user-message"),
        html.P(f"Asistente: {respuesta['respuesta']['output']}", className="bot-message")
    ]
    
    # Cambiar página si es necesario (la funcionalidad está en respuesta['funcionalidad'])
    # Esto se manejará con otro callback
    
    return new_messages, ""

# Callback para actualizar la URL según la funcionalidad activa
@callback(
    Output('url', 'pathname'),
    Input('chat-messages', 'children')
)
def update_url(messages):
    if not messages:
        return '/'
    
    # Obtener la última respuesta del orquestador (necesitarías almacenar esto)
    # Esto es un placeholder - necesitarías un mecanismo para almacenar el estado
    return '/'

if __name__ == '__main__':
    app.run(debug=True)