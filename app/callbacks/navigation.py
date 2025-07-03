"""
Callbacks específicos para la navegación y vista funcional
"""

import dash
from dash import Input, Output, State, callback
from styles.functional_view import FUNCTIONAL_VIEW_STYLES
from components.functional_view import (
    create_diagnostico_content,
    create_explicacion_content,
    create_interpretacion_examenes_content,
    create_contacto_medico_content,
    create_busqueda_content,
    create_analizar_imagenes_content
)
from components.chat import create_chat_component
from components.functional_view import create_functional_view_component

def register_navigation_callbacks(app):
    """Registra todos los callbacks relacionados con la navegación"""
    
    @app.callback(
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
            functional_style = {**FUNCTIONAL_VIEW_STYLES['functional-view'], **FUNCTIONAL_VIEW_STYLES['functional-view-hidden']}
            return functional_style, None
        
        if pathname == '/' and functionality == 'home':
            # Ocultar vista funcional
            functional_style = {**FUNCTIONAL_VIEW_STYLES['functional-view'], **FUNCTIONAL_VIEW_STYLES['functional-view-hidden']}
            return functional_style, None
        
        # Mostrar vista funcional
        functional_style = FUNCTIONAL_VIEW_STYLES['functional-view']
        
        # Determinar qué contenido mostrar basado en la funcionalidad
        if pathname == '/diagnostico' or functionality == 'diagnostico':
            content = create_diagnostico_content()
        elif pathname == '/explicacion' or functionality == 'explicacion_medica':
            content = create_explicacion_content()
        elif pathname == '/interpretacion-examenes' or functionality == 'interpretacion_examenes':
            content = create_interpretacion_examenes_content()
        elif pathname == '/contacto-medico' or functionality == 'contacto_medico':
            content = create_contacto_medico_content()
        elif pathname == '/busqueda' or functionality == 'busqueda':
            content = create_busqueda_content()
        elif pathname == '/analizar-imagenes' or functionality == 'analizar_imagenes':
            content = create_analizar_imagenes_content()
        else:
            content = dash.html.Div([
                dash.html.H4("Funcionalidad no reconocida", style={'color': '#b19cd9'}),
                dash.html.P("La funcionalidad solicitada no está disponible.")
            ])
        
        return functional_style, content

    @app.callback(
        Output('url', 'pathname'),
        Input('diagnostico-button', 'n_clicks'),
        Input('explicacion-button', 'n_clicks'),
        Input('interpretacion-examenes-button', 'n_clicks'),
        Input('resumen-medico-button', 'n_clicks'),
        Input('contacto-medico-button', 'n_clicks'),
        Input('busqueda-button', 'n_clicks'),
        Input('analizar-imagenes-button', 'n_clicks')
    )
    def navigate_to_functionality(diagnostico_clicks, explicacion_clicks, interpretacion_clicks, 
                                resumen_clicks, contacto_clicks, busqueda_clicks, analizar_clicks):
        ctx = dash.callback_context
        if not ctx.triggered:
            return '/'
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Mapear botones a rutas
        route_mapping = {
            'diagnostico-button': '/diagnostico',
            'explicacion-button': '/explicacion',
            'interpretacion-examenes-button': '/interpretacion-examenes',
            'resumen-medico-button': '/resumen-medico',
            'contacto-medico-button': '/contacto-medico',
            'busqueda-button': '/busqueda',
            'analizar-imagenes-button': '/analizar-imagenes'
        }
        
        return route_mapping.get(button_id, '/')

    @app.callback(
        Output('main-content-router', 'children'),
        Input('url', 'pathname')
    )
    def route_main_content(pathname):
        if pathname == '/':
            return create_chat_component()
        elif pathname == '/chat':
            return create_chat_component()
        elif pathname == '/vista-funcional':
            return create_functional_view_component()
        else:
            return create_chat_component() 