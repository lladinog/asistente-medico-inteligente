import os
import sys
import datetime
from dash.exceptions import PreventUpdate
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
from dash import dcc, html, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
from agents.orquestador import Orquestador, FuncionalidadMedica
from agents.diagnostico import AgenteDiagnostico
from agents.explicacion import AgenteExplicacionMedica

# Configuración inicial
config = {
    "nombre_app": "Asistente Médico Rural",
    "estilo": dbc.themes.DARKLY  # Cambiamos a tema oscuro
}

model_config = {
    "model_path": "modelos/llama-medical.bin",
    "n_ctx": 5000,
    "n_threads": 8
}

# Inicializar orquestador
orquestador = Orquestador(config, model_config)

# Registrar agentes
orquestador.registrar_agente(
    FuncionalidadMedica.DIAGNOSTICO,
    AgenteDiagnostico()
)
orquestador.registrar_agente(
    FuncionalidadMedica.EXPLICACION_MEDICA,
    AgenteExplicacionMedica()
)

# Crear aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[config["estilo"]])
app.title = config["nombre_app"]

# Estilos personalizados
styles = {
    'main-container': {
        'backgroundColor': '#0f0f17',
        'color': '#ffffff',
        'minHeight': '100vh',
        'padding': '20px'
    },
    'chat-container': {
        'backgroundColor': '#1a1a3a',
        'borderRadius': '10px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
        'height': '80vh',
        'display': 'flex',
        'flexDirection': 'column'
    },
    'chat-header': {
        'backgroundColor': '#6a0dad',
        'color': 'white',
        'padding': '15px',
        'borderTopLeftRadius': '10px',
        'borderTopRightRadius': '10px',
        'fontWeight': 'bold',
        'fontSize': '1.2rem'
    },
    'chat-messages': {
        'flexGrow': 1,
        'overflowY': 'auto',
        'padding': '20px',
        'background': 'linear-gradient(to bottom, #1a1a3a, #2a2a4a)'
    },
    'message-input': {
        'padding': '15px',
        'borderTop': '1px solid #444',
        'backgroundColor': '#2a2a4a'
    },
    'user-message': {
        'backgroundColor': '#6a0dad',
        'color': 'white',
        'padding': '10px 15px',
        'borderRadius': '18px',
        'marginBottom': '10px',
        'maxWidth': '80%',
        'alignSelf': 'flex-end',
        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'
    },
    'bot-message': {
        'backgroundColor': '#3a3a5a',
        'color': 'white',
        'padding': '10px 15px',
        'borderRadius': '18px',
        'marginBottom': '10px',
        'maxWidth': '80%',
        'alignSelf': 'flex-start',
        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'
    },
    'welcome-message': {
        'textAlign': 'center',
        'padding': '20px',
        'color': '#b19cd9',
        'fontStyle': 'italic'
    },
    'functional-view': {
        'backgroundColor': '#151525',
        'borderRadius': '10px',
        'padding': '20px',
        'height': '80vh',
        'overflowY': 'auto',
        'marginLeft': '10px'
    },
    'upload-button': {
        'backgroundColor': '#3a3a5a',
        'border': 'none',
        'borderRadius': '5px',
        'marginRight': '10px',
        'cursor': 'pointer'
    }
}

# Layout principal mejorado
app.layout = dbc.Container(fluid=True, style=styles['main-container'], children=[
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-id', storage_type='session'),
    dcc.Store(id='current-functionality', data='home'),
    dcc.Upload(id='upload-document', children=None, multiple=True),
    
    # Header mejorado
    dbc.Navbar(
        dbc.Container([
            html.Div(
                [
                    html.Img(src='/assets/medical-icon.png', height="30px", style={'marginRight': '10px'}),
                    html.H4("Asistente Médico Rural", className="ms-2", style={'color': '#b19cd9'})
                ],
                className="d-flex align-items-center"
            ),
            dbc.Nav([
                dbc.NavLink("Inicio", href="/", active="exact", style={'color': '#d3bcf6'}),
                dbc.NavLink("Diagnóstico", href="/diagnostico", style={'color': '#d3bcf6'}),
                dbc.NavLink("Explicaciones", href="/explicacion", style={'color': '#d3bcf6'})
            ], navbar=True)
        ]),
        color='#1a1a3a',
        dark=True,
        sticky='top',
        className='mb-4'
    ),
    
    # Contenido principal con vista dividida
    dbc.Row([
        # Chat (siempre visible)
        dbc.Col(
            dbc.Card(style=styles['chat-container'], children=[
                dbc.CardHeader("Chat de Consulta Médica", style=styles['chat-header']),
                dbc.CardBody([
                    html.Div(id='chat-messages', style=styles['chat-messages'], children=[
                        html.Div(style=styles['welcome-message'], children=[
                            html.H5("Bienvenido al Asistente Médico Rural"),
                            html.P("Soy tu asistente de salud virtual. ¿En qué puedo ayudarte hoy?"),
                            html.P("Puedes preguntarme sobre síntomas, diagnósticos o explicaciones médicas.")
                        ])
                    ]),
                    dbc.InputGroup(style=styles['message-input'], children=[
                        dbc.Button(
                            html.I(className="fas fa-paperclip"),
                            id='upload-button',
                            style=styles['upload-button']
                        ),
                        dbc.Input(
                            id='user-input',
                            placeholder="Escribe tu consulta médica...",
                            type="text",
                            style={
                                'backgroundColor': '#3a3a5a',
                                'color': 'white',
                                'border': 'none',
                                'borderRadius': '20px',
                                'padding': '10px 15px',
                                'flexGrow': 1
                            }
                        ),
                        dbc.Button(
                            "Enviar",
                            id='send-button',
                            color="primary",
                            style={
                                'backgroundColor': '#6a0dad',
                                'border': 'none',
                                'borderRadius': '20px',
                                'marginLeft': '10px'
                            }
                        )
                    ])
                ])
            ]),
            width=6,  # Mitad del ancho cuando hay vista funcional
            id='chat-column'
        ),
        
        # Vista funcional (dinámica)
        dbc.Col(
            html.Div(id='functional-content', style=styles['functional-view']),
            width=6,
            id='functional-column',
            style={'display': 'none'}  # Oculto por defecto
        )
    ])
])

# Callback para manejar la subida de documentos
@callback(
    Output('upload-document', 'children'),
    Input('upload-button', 'n_clicks'),
    prevent_initial_call=True
)
def trigger_upload(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    return no_update

# Callback para mostrar/ocultar vista funcional
@callback(
    [Output('functional-column', 'style'),
     Output('functional-content', 'children'),
     Output('chat-column', 'width')],
    [Input('url', 'pathname'),
     Input('current-functionality', 'data')],
    prevent_initial_call=True
)
def toggle_functional_view(pathname, functionality):
    if pathname == '/' and functionality == 'home':
        # Vista de chat completa
        return {'display': 'none'}, None, 12
    
    # Vista dividida
    if pathname == '/diagnostico' or functionality == FuncionalidadMedica.DIAGNOSTICO.value:
        content = html.Div([
            html.H4("Diagnóstico Médico", style={'color': '#b19cd9'}),
            html.P("Aquí aparecerá el análisis detallado de tus síntomas."),
            # Componentes específicos de diagnóstico...
        ])
    elif pathname == '/explicacion' or functionality == FuncionalidadMedica.EXPLICACION_MEDICA.value:
        content = html.Div([
            html.H4("Explicación Médica", style={'color': '#b19cd9'}),
            html.P("Aquí aparecerán las explicaciones detalladas de términos médicos."),
            # Componentes específicos de explicación...
        ])
    else:
        content = html.Div([
            html.H4("Funcionalidad no reconocida", style={'color': '#b19cd9'}),
            html.P("La funcionalidad solicitada no está disponible.")
        ])
    
    return {'display': 'block'}, content, 6

# Callback para manejar el chat
@callback(
    [Output('chat-messages', 'children'),
     Output('user-input', 'value'),
     Output('current-functionality', 'data'),
     Output('url', 'pathname')],
    [Input('send-button', 'n_clicks'),
     Input('user-input', 'n_submit')],
    [State('user-input', 'value'),
     State('session-id', 'data'),
     State('chat-messages', 'children'),
     State('current-functionality', 'data')],
    prevent_initial_call=True
)
def update_chat(n_clicks, n_submit, user_input, session_id, existing_messages, current_functionality):
    if not user_input or (n_clicks is None and n_submit is None):
        raise PreventUpdate
    
    try:
        # Obtener o crear session_id
        if not session_id:
            session_id = orquestador._generar_session_id()
        
        # Procesar mensaje con el orquestador
        respuesta = orquestador.procesar_mensaje(session_id, user_input)
        funcionalidad = respuesta.get('funcionalidad', 'home')
        output = respuesta['respuesta'].get('output', 'No se pudo generar una respuesta.')
        
        # Eliminar mensaje de bienvenida si es el primer mensaje
        if existing_messages and len(existing_messages) == 1 and 'welcome-message' in existing_messages[0]['props']['style']:
            existing_messages = []
        
        # Actualizar mensajes del chat
        new_messages = (existing_messages or []) + [
            html.Div(f"Tú: {user_input}", style=styles['user-message']),
            html.Div(f"Asistente: {output}", style=styles['bot-message'])
        ]
        
        # Determinar si necesitamos cambiar de página
        if funcionalidad != current_functionality:
            if funcionalidad == FuncionalidadMedica.DIAGNOSTICO.value:
                pathname = '/diagnostico'
            elif funcionalidad == FuncionalidadMedica.EXPLICACION_MEDICA.value:
                pathname = '/explicacion'
            else:
                pathname = '/'
        else:
            pathname = dash.no_update
        
        return new_messages, "", funcionalidad, pathname
    
    except Exception as e:
        print(f"Error en update_chat: {str(e)}")
        error_message = html.Div(
            "Lo siento, ocurrió un error al procesar tu mensaje. Por favor intenta nuevamente.",
            style=styles['bot-message']
        )
        new_messages = (existing_messages or []) + [
            html.Div(f"Tú: {user_input}", style=styles['user-message']),
            error_message
        ]
        return new_messages, "", current_functionality, dash.no_update

if __name__ == '__main__':
    app.run(debug=True)