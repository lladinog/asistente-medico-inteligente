"""
Callbacks específicos para el componente Chat
"""

import dash
from dash import Input, Output, State, callback, no_update, ALL
from dash.exceptions import PreventUpdate
import datetime
from styles.chat import CHAT_STYLES
from utils.funcionalidades import FuncionalidadMedica
import uuid
from app.util.helpers import generar_mensaje_bienvenida, create_conversation_item
import time

def register_chat_callbacks(app, orquestador):
    """Registra todos los callbacks relacionados con el chat"""
    
    @app.callback(
        [Output('chat-messages', 'children', allow_duplicate=True),
         Output('user-input', 'value'),
         Output('current-functionality', 'data'),
         Output('url', 'pathname', allow_duplicate=True),
         Output('conversations-store', 'data'),
         Output('session-id', 'data'),
         Output('sidebar-editing-title', 'data', allow_duplicate=True)],
        [Input('send-button', 'n_clicks'),
         Input('user-input', 'n_submit'),
         Input('new-chat-button', 'n_clicks'),
         Input({'type': 'save-title-btn', 'index': ALL}, 'n_clicks'),
         Input({'type': 'conversation-title-input', 'index': ALL}, 'n_blur')],
        [State('user-input', 'value'),
         State('session-id', 'data'),
         State('chat-messages', 'children'),
         State('current-functionality', 'data'),
         State('conversations-store', 'data'),
         State({'type': 'conversation-title-input', 'index': ALL}, 'value'),
         State('sidebar-editing-title', 'data')],
        prevent_initial_call=True
    )
    def update_chat(send_clicks, submit, new_chat_clicks, save_title_clicks, input_blur, user_input, session_id, existing_messages, current_functionality, conversations, input_values, editing_title):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # EDICIÓN DE TÍTULO
        if 'save-title-btn' in trigger_id or 'conversation-title-input' in trigger_id:
            if not editing_title or not conversations:
                raise PreventUpdate
            new_title = input_values[0] if input_values else None
            if new_title:
                for conv in conversations:
                    if conv['id'] == editing_title:
                        conv['title'] = new_title
                # No cambiamos mensajes ni funcionalidad, solo actualizamos el store y salimos del modo edición
                return no_update, no_update, no_update, no_update, conversations, no_update, None
            raise PreventUpdate
        
        # Manejar nueva conversación
        if trigger_id == 'new-chat-button':
            new_session_id = str(uuid.uuid4())
            bienvenida = generar_mensaje_bienvenida()
            welcome_message = [
                dash.html.Pre(f"Asistente: {bienvenida}", style=CHAT_STYLES['bot-message'])
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
            return welcome_message, "", 'home', '/', conversations, new_session_id, None
        
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
            
            return rendered_messages, "", funcionalidad, pathname, conversations, session_id, None
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
            return rendered_messages, "", current_functionality, dash.no_update, conversations, session_id, None 