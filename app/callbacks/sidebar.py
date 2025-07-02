"""
Callbacks específicos para el componente Sidebar
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
from dash import Input, Output, State, callback
from styles.sidebar import SIDEBAR_STYLES

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
        Input('conversations-store', 'data')
    )
    def update_conversations_list(conversations):
        if not conversations:
            return []
        
        # Ordenar conversaciones por timestamp (más reciente primero)
        sorted_conv = sorted(conversations, key=lambda x: x['timestamp'], reverse=True)
        
        return [
            dash.html.Div(
                conv['title'],
                style=SIDEBAR_STYLES['conversation-item'],
                id={'type': 'conversation-item', 'index': conv['id']}
            )
            for conv in sorted_conv
        ] 