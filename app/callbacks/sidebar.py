"""
Callbacks específicos para el componente Sidebar
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
from dash import Input, Output, State, callback, MATCH, ALL
from styles.sidebar import SIDEBAR_STYLES
from dash import dcc, html
import dash_bootstrap_components as dbc
import json

def register_sidebar_callbacks(app):
    """Registra todos los callbacks relacionados con el sidebar"""
    
    @app.callback(
        Output('sidebar', 'style'),
        Output('sidebar-collapsed', 'data'),
        Output('sidebar-toggle', 'style'),
        Output('floating-sidebar-toggle', 'style'),
        Input('sidebar-toggle', 'n_clicks'),
        Input('floating-sidebar-toggle', 'n_clicks'),
        State('sidebar-collapsed', 'data')
    )
    def toggle_sidebar(sidebar_clicks, floating_clicks, is_collapsed):
        ctx = dash.callback_context
        if not ctx.triggered:
            return SIDEBAR_STYLES['sidebar'], False, SIDEBAR_STYLES['sidebar-toggle'], {'display': 'none'}
        
        # Determinar nuevo estado
        new_collapsed = not is_collapsed
        
        if new_collapsed:
            sidebar_style = {**SIDEBAR_STYLES['sidebar'], **SIDEBAR_STYLES['sidebar-hidden']}
            toggle_style = {**SIDEBAR_STYLES['sidebar-toggle'], 'display': 'none'}
            floating_style = {'display': 'flex', 'position': 'fixed', 'left': '10px', 'top': '10px', 'backgroundColor': '#6a0dad', 'border': 'none', 'color': 'white', 'borderRadius': '5px', 'width': '30px', 'height': '30px', 'cursor': 'pointer', 'zIndex': 1000, 'alignItems': 'center', 'justifyContent': 'center'}
        else:
            sidebar_style = SIDEBAR_STYLES['sidebar']
            toggle_style = SIDEBAR_STYLES['sidebar-toggle']
            floating_style = {'display': 'none'}
        
        return sidebar_style, new_collapsed, toggle_style, floating_style

    @app.callback(
        Output('conversations-list', 'children'),
        Input('conversations-store', 'data'),
        State('session-id', 'data'),
        State('sidebar-editing-title', 'data')
    )
    def update_conversations_list(conversations, active_session_id, editing_title):
        if not conversations:
            return []
        sorted_conv = sorted(conversations, key=lambda x: x['timestamp'], reverse=True)
        items = []
        for conv in sorted_conv:
            is_editing = editing_title == conv['id']
            if is_editing:
                # Input para editar el título
                items.append(
                    dash.html.Div([
                        dcc.Input(
                            id={'type': 'conversation-title-input', 'index': conv['id']},
                            value=conv['title'],
                            debounce=True,
                            style={'width': '80%', 'fontSize': '14px', 'marginRight': '4px'}
                        ),
                        dbc.Button(
                            html.I(className='fas fa-check'),
                            id={'type': 'save-title-btn', 'index': conv['id']},
                            size='sm', color='success', style={'padding': '2px 6px', 'fontSize': '12px'}
                        )
                    ], style=SIDEBAR_STYLES['conversation-item'], id={'type': 'conversation-item', 'index': conv['id']})
                )
            else:
                items.append(
                    dash.html.Div([
                        dash.html.Span(
                            conv['title'],
                            id={'type': 'conversation-title', 'index': conv['id']},
                            n_clicks=0,
                            style={'cursor': 'pointer', 'marginRight': '4px'}
                        ),
                        dbc.Button(
                            html.I(className='fas fa-pen'),
                            id={'type': 'edit-title-btn', 'index': conv['id']},
                            size='sm', color='secondary', style={'padding': '2px 6px', 'fontSize': '12px'}
                        )
                    ], style=SIDEBAR_STYLES['conversation-item'], id={'type': 'conversation-item', 'index': conv['id']})
                )
        return items

    # Callback para activar el modo edición al hacer clic en el texto o el botón
    @app.callback(
        Output('sidebar-editing-title', 'data'),
        [Input({'type': 'edit-title-btn', 'index': ALL}, 'n_clicks'),
         Input({'type': 'conversation-title', 'index': ALL}, 'n_clicks')],
        [State('conversations-store', 'data')],
        prevent_initial_call=True
    )
    def set_editing_title(edit_btns, title_clicks, conversations):
        ctx = dash.callback_context
        if not ctx.triggered or not conversations:
            raise dash.exceptions.PreventUpdate
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        try:
            trigger_id = json.loads(trigger)
            conv_id = trigger_id['index']
            return conv_id
        except Exception:
            raise dash.exceptions.PreventUpdate 