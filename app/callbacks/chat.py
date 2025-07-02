"""
Callbacks específicos para el componente Chat
"""

import dash
from dash import Input, Output, State, callback, no_update
from dash.exceptions import PreventUpdate
import datetime
from styles.chat import CHAT_STYLES
from agents.utils.funcionalidades import FuncionalidadMedica
import uuid
from app.utils.helpers import generar_mensaje_bienvenida, create_conversation_item
import time

FUNCIONALIDAD_ICONS = {
    'diagnostico': ("🔍", "Diagnóstico médico"),
    'analisis_imagenes': ("🖼️", "Análisis de imágenes"),
    'interpretacion_examenes': ("🔬", "Interpretación de exámenes"),
    'explicacion': ("📚", "Explicación médica"),
    'buscador_centros': ("🏥", "Buscador de centros médicos"),
    'contacto_medico': ("👨‍⚕️", "Contacto médico")
}

def register_chat_callbacks(app, orquestador):
    """Registra todos los callbacks relacionados con el chat"""
    
    @app.callback(
        [Output('chat-messages', 'children', allow_duplicate=True),
         Output('user-input', 'value'),
         Output('current-functionality', 'data'),
         Output('url', 'pathname', allow_duplicate=True),
         Output('conversations-store', 'data'),
         Output('session-id', 'data')],
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
        
        # Manejar nueva conversación
        if trigger_id == 'new-chat-button':
            new_session_id = str(uuid.uuid4())
            bienvenida = generar_mensaje_bienvenida()
            welcome_message = [
                dash.html.Div(f"Asistente: {bienvenida}", style=CHAT_STYLES['bot-message'])
            ]
            # Crear nueva conversación con los campos correctos
            new_conversation = create_conversation_item("Nueva conversación", new_session_id)
            new_conversation.update({
                'session_id': new_session_id,
                'messages': [
                    {'role': 'assistant', 'content': bienvenida}
                ],
                'active': True
            })
            # Desactivar otras conversaciones
            if conversations is None:
                conversations = []
            for conv in conversations:
                conv['active'] = False
            conversations.append(new_conversation)
            return welcome_message, "", 'home', '/', conversations, new_session_id
        
        # Manejar envío de mensaje
        if not user_input or (send_clicks is None and submit is None):
            raise PreventUpdate
        
        # Buscar la conversación activa
        if not conversations:
            raise PreventUpdate
        conv = next((c for c in conversations if c['session_id'] == session_id), None)
        if not conv:
            raise PreventUpdate
        
        # Añadir mensaje del usuario
        conv['messages'].append({'role': 'user', 'content': user_input})
        
        try:
            # Procesar mensaje con el orquestador usando el session_id de la conversación
            respuesta = orquestador.procesar_mensaje(session_id, user_input)
            funcionalidad = respuesta.get('funcionalidad', 'home')
            output = respuesta['respuesta'].get('output', 'No se pudo generar una respuesta.')
            
            # Añadir respuesta del asistente
            conv['messages'].append({'role': 'assistant', 'content': output})
            
            # Renderizar mensajes de la conversación activa
            rendered_messages = []
            for msg in conv['messages']:
                if msg['role'] == 'user':
                    rendered_messages.append(dash.html.Div(f"Tú: {msg['content']}", style=CHAT_STYLES['user-message']))
                else:
                    rendered_messages.append(dash.html.Div(f"Asistente: {msg['content']}", style=CHAT_STYLES['bot-message']))
            
            # Determinar si necesitamos cambiar de página
            if funcionalidad != current_functionality:
                route_mapping = {
                    'diagnostico': '/diagnostico',
                    'explicacion_medica': '/explicacion',
                    'explicacion': '/explicacion',
                    'interpretacion_examenes': '/interpretacion-examenes',
                    'resumen_medico': '/resumen-medico',
                    'contacto_medico': '/contacto-medico',
                    'buscador_centros': '/busqueda',
                    'busqueda': '/busqueda',
                    'analisis_imagenes': '/analizar-imagenes',
                    'analizar_imagenes': '/analizar-imagenes'
                }
                pathname = route_mapping.get(funcionalidad, '/')
            else:
                pathname = dash.no_update
            
            return rendered_messages, "", funcionalidad, pathname, conversations, session_id
        except Exception as e:
            print(f"Error en update_chat: {str(e)}")
            error_message = dash.html.Div(
                "Lo siento, ocurrió un error al procesar tu mensaje. Por favor intenta nuevamente.",
                style=CHAT_STYLES['bot-message']
            )
            conv['messages'].append({'role': 'assistant', 'content': "Lo siento, ocurrió un error al procesar tu mensaje. Por favor intenta nuevamente."})
            rendered_messages = []
            for msg in conv['messages']:
                if msg['role'] == 'user':
                    rendered_messages.append(dash.html.Div(f"Tú: {msg['content']}", style=CHAT_STYLES['user-message']))
                else:
                    rendered_messages.append(dash.html.Div(f"Asistente: {msg['content']}", style=CHAT_STYLES['bot-message']))
            return rendered_messages, "", current_functionality, dash.no_update, conversations, session_id 