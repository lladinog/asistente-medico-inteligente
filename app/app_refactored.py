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

# Importar componentes
from components.sidebar import create_sidebar_component
from components.chat import create_chat_component
from components.functional_view import create_functional_view_component, create_diagnostico_content, create_explicacion_content

# Configuración inicial
config = {
    "nombre_app": "Asistente Médico Rural",
    "estilo": dbc.themes.DARKLY
}

model_config = {
    "model_path": "modelos/llama-medical.bin",
    "n_ctx": 2048,
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

# Estilos del layout principal
main_styles = {
    'main-container': {
        'backgroundColor': '#0f0f17',
        'color': '#ffffff',
        'minHeight': '100vh',
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

# Layout principal con componentes
app.layout = html.Div(style=main_styles['main-container'], children=[
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-id', storage_type='session'),
    dcc.Store(id='current-functionality', data='home'),
    dcc.Store(id='sidebar-collapsed', data=False),
    dcc.Store(id='conversations-store', data=[]),
    dcc.Upload(id='upload-document', children=None, multiple=True),
    
    # Botón flotante para abrir sidebar (visible cuando está cerrado)
    dbc.Button(
        html.I(className="fas fa-bars"),
        id='floating-sidebar-toggle',
        style=main_styles['floating-sidebar-toggle']
    ),
    
    # Sidebar
    create_sidebar_component(),
    
    # Chat principal
    create_chat_component(),
    
    # Vista funcional
    create_functional_view_component()
])

# Callbacks para manejar la interactividad del sidebar
@callback(
    Output('sidebar', 'style'),
    Output('sidebar-collapsed', 'data'),
    Output('sidebar-toggle', 'style'),
    Output('floating-sidebar-toggle', 'style'),
    Input('sidebar-toggle', 'n_clicks'),
    Input('mobile-sidebar-toggle', 'n_clicks'),
    Input('floating-sidebar-toggle', 'n_clicks'),
    State('sidebar-collapsed', 'data')
)
def toggle_sidebar(sidebar_clicks, mobile_clicks, floating_clicks, is_collapsed):
    ctx = dash.callback_context
    if not ctx.triggered:
        return {'width': '300px', 'backgroundColor': '#1a1a3a', 'padding': '15px', 'borderRight': '1px solid #444', 'transition': 'all 0.3s ease', 'overflowY': 'auto', 'height': '100vh', 'position': 'relative', 'zIndex': 10, 'flexShrink': 0}, False, {'position': 'absolute', 'right': '-40px', 'top': '10px', 'backgroundColor': '#6a0dad', 'border': 'none', 'color': 'white', 'borderRadius': '5px', 'width': '30px', 'height': '30px', 'cursor': 'pointer', 'zIndex': 1000, 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}, {'display': 'none'}
    
    # Determinar nuevo estado
    new_collapsed = not is_collapsed
    
    if new_collapsed:
        sidebar_style = {'transform': 'translateX(-100%)', 'width': '0', 'padding': '0', 'borderRight': 'none', 'backgroundColor': '#1a1a3a', 'transition': 'all 0.3s ease', 'overflowY': 'auto', 'height': '100vh', 'position': 'relative', 'zIndex': 10, 'flexShrink': 0}
        toggle_style = {'display': 'none'}
        floating_style = {'display': 'flex', 'position': 'fixed', 'left': '10px', 'top': '10px', 'backgroundColor': '#6a0dad', 'border': 'none', 'color': 'white', 'borderRadius': '5px', 'width': '30px', 'height': '30px', 'cursor': 'pointer', 'zIndex': 1000, 'alignItems': 'center', 'justifyContent': 'center'}
    else:
        sidebar_style = {'width': '300px', 'backgroundColor': '#1a1a3a', 'padding': '15px', 'borderRight': '1px solid #444', 'transition': 'all 0.3s ease', 'overflowY': 'auto', 'height': '100vh', 'position': 'relative', 'zIndex': 10, 'flexShrink': 0}
        toggle_style = {'position': 'absolute', 'right': '-40px', 'top': '10px', 'backgroundColor': '#6a0dad', 'border': 'none', 'color': 'white', 'borderRadius': '5px', 'width': '30px', 'height': '30px', 'cursor': 'pointer', 'zIndex': 1000, 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}
        floating_style = {'display': 'none'}
    
    return sidebar_style, new_collapsed, toggle_style, floating_style

# Callback para manejar la vista funcional
@callback(
    Output('functional-view', 'style'),
    Output('functional-content', 'children'),
    Input('url', 'pathname'),
    Input('current-functionality', 'data'),
    Input('functional-close-button', 'n_clicks')
)
def update_functional_view(pathname, functionality, close_clicks):
    ctx = dash.callback_context
    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'functional-close-button.n_clicks':
        # Cerrar vista funcional
        functional_style = {'width': '0', 'padding': '0', 'borderLeft': 'none', 'overflow': 'hidden', 'backgroundColor': '#151525', 'flexShrink': 0, 'transition': 'all 0.3s ease', 'display': 'flex', 'flexDirection': 'column'}
        return functional_style, None
    
    if pathname == '/' and functionality == 'home':
        # Ocultar vista funcional
        functional_style = {'width': '0', 'padding': '0', 'borderLeft': 'none', 'overflow': 'hidden', 'backgroundColor': '#151525', 'flexShrink': 0, 'transition': 'all 0.3s ease', 'display': 'flex', 'flexDirection': 'column'}
        return functional_style, None
    
    # Mostrar vista funcional
    functional_style = {'width': '400px', 'backgroundColor': '#151525', 'borderLeft': '1px solid #444', 'overflowY': 'auto', 'padding': '20px', 'flexShrink': 0, 'transition': 'all 0.3s ease', 'display': 'flex', 'flexDirection': 'column'}
    
    if pathname == '/diagnostico' or functionality == FuncionalidadMedica.DIAGNOSTICO.value:
        content = create_diagnostico_content()
    elif pathname == '/explicacion' or functionality == FuncionalidadMedica.EXPLICACION_MEDICA.value:
        content = create_explicacion_content()
    else:
        content = html.Div([
            html.H4("Funcionalidad no reconocida", style={'color': '#b19cd9'}),
            html.P("La funcionalidad solicitada no está disponible.")
        ])
    
    return functional_style, content

# Callback para navegación
@callback(
    Output('url', 'pathname'),
    Input('diagnostico-button', 'n_clicks'),
    Input('explicacion-button', 'n_clicks')
)
def navigate_to_functionality(diagnostico_clicks, explicacion_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return '/'
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'diagnostico-button':
        return '/diagnostico'
    elif button_id == 'explicacion-button':
        return '/explicacion'
    
    return '/'

# Callback para manejar el chat
@callback(
    [Output('chat-messages', 'children', allow_duplicate=True),
     Output('user-input', 'value'),
     Output('current-functionality', 'data'),
     Output('url', 'pathname', allow_duplicate=True),
     Output('conversations-store', 'data')],
    [Input('send-button', 'n_clicks'),
     Input('user-input', 'n_submit'),
     Input('new-chat-button', 'n_clicks')],
    [State('user-input', 'value'),
     State('session-id', 'data'),
     State('chat-messages', 'children'),
     State('current-functionality', 'data'),
     State('conversations-store', 'data')],
    prevent_initial_call=True
)
def update_chat(send_clicks, submit, new_chat_clicks, user_input, session_id, existing_messages, current_functionality, conversations):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Manejar nuevo chat
    if trigger_id == 'new-chat-button':
        new_session_id = orquestador._generar_session_id()
        welcome_message = html.Div(style={'textAlign': 'center', 'padding': '20px', 'color': '#b19cd9'}, children=[
            html.H5("Bienvenido al Asistente Médico Rural"),
            html.P("Soy tu asistente de salud virtual. ¿En qué puedo ayudarte hoy?"),
            html.P("Puedes preguntarme sobre síntomas, diagnósticos o explicaciones médicas.")
        ])
        
        # Agregar nueva conversación al historial
        new_conversation = {
            'id': new_session_id,
            'title': 'Nueva conversación',
            'timestamp': datetime.datetime.now().isoformat()
        }
        updated_conversations = conversations + [new_conversation]
        
        return [welcome_message], "", 'home', '/', updated_conversations
    
    # Manejar envío de mensaje
    if not user_input or (send_clicks is None and submit is None):
        raise PreventUpdate
    
    try:
        # Obtener o crear session_id
        if not session_id:
            session_id = orquestador._generar_session_id()
        
        # Procesar mensaje con el orquestador
        respuesta = orquestador.procesar_mensaje(session_id, user_input)
        funcionalidad = respuesta.get('funcionalidad', 'home')
        output = respuesta['respuesta'].get('output', 'No se pudo generar una respuesta.')
        
        # Estilos para mensajes
        user_style = {'backgroundColor': '#6a0dad', 'color': 'white', 'padding': '12px 16px', 'borderRadius': '18px 18px 4px 18px', 'marginBottom': '10px', 'maxWidth': '80%', 'alignSelf': 'flex-end', 'boxShadow': '0 1px 2px rgba(0,0,0,0.1)', 'wordWrap': 'break-word'}
        bot_style = {'backgroundColor': '#2a2a4a', 'color': 'white', 'padding': '12px 16px', 'borderRadius': '18px 18px 18px 4px', 'marginBottom': '10px', 'maxWidth': '80%', 'alignSelf': 'flex-start', 'boxShadow': '0 1px 2px rgba(0,0,0,0.1)', 'wordWrap': 'break-word'}
        
        # Actualizar mensajes del chat
        new_messages = (existing_messages or []) + [
            html.Div(f"Tú: {user_input}", style=user_style),
            html.Div(f"Asistente: {output}", style=bot_style)
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
        
        # Actualizar conversaciones si es un nuevo mensaje en una conversación existente
        updated_conversations = conversations
        if session_id and conversations:
            # Actualizar el título de la conversación con el primer mensaje
            if not any(conv['id'] == session_id for conv in conversations):
                new_conversation = {
                    'id': session_id,
                    'title': user_input[:50] + ('...' if len(user_input) > 50 else ''),
                    'timestamp': datetime.datetime.now().isoformat()
                }
                updated_conversations = conversations + [new_conversation]
        
        return new_messages, "", funcionalidad, pathname, updated_conversations
    
    except Exception as e:
        print(f"Error en update_chat: {str(e)}")
        error_message = html.Div(
            "Lo siento, ocurrió un error al procesar tu mensaje. Por favor intenta nuevamente.",
            style={'backgroundColor': '#2a2a4a', 'color': 'white', 'padding': '12px 16px', 'borderRadius': '18px 18px 18px 4px', 'marginBottom': '10px', 'maxWidth': '80%', 'alignSelf': 'flex-start', 'boxShadow': '0 1px 2px rgba(0,0,0,0.1)', 'wordWrap': 'break-word'}
        )
        new_messages = (existing_messages or []) + [
            html.Div(f"Tú: {user_input}", style={'backgroundColor': '#6a0dad', 'color': 'white', 'padding': '12px 16px', 'borderRadius': '18px 18px 4px 18px', 'marginBottom': '10px', 'maxWidth': '80%', 'alignSelf': 'flex-end', 'boxShadow': '0 1px 2px rgba(0,0,0,0.1)', 'wordWrap': 'break-word'}),
            error_message
        ]
        return new_messages, "", current_functionality, dash.no_update, conversations

# Callback para actualizar la lista de conversaciones
@callback(
    Output('conversations-list', 'children'),
    Input('conversations-store', 'data')
)
def update_conversations_list(conversations):
    if not conversations:
        return []
    
    # Ordenar conversaciones por timestamp (más reciente primero)
    sorted_conv = sorted(conversations, key=lambda x: x['timestamp'], reverse=True)
    
    conversation_style = {'padding': '10px', 'marginBottom': '5px', 'borderRadius': '5px', 'cursor': 'pointer', 'backgroundColor': '#2a2a4a', 'overflow': 'hidden', 'textOverflow': 'ellipsis', 'whiteSpace': 'nowrap', 'transition': 'all 0.2s ease'}
    
    return [
        html.Div(
            conv['title'],
            style=conversation_style,
            id={'type': 'conversation-item', 'index': conv['id']}
        )
        for conv in sorted_conv
    ]

if __name__ == '__main__':
    app.run(debug=True) 