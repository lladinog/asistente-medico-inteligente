import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

def create_functional_view_component():
    """Crea el componente FunctionalView"""
    
    styles = {
        'functional-view': {
            'width': '400px',
            'backgroundColor': '#151525',
            'borderLeft': '1px solid #444',
            'overflowY': 'auto',
            'padding': '20px',
            'flexShrink': 0,
            'transition': 'all 0.3s ease',
            'display': 'flex',
            'flexDirection': 'column'
        },
        'functional-view-hidden': {
            'width': '0',
            'padding': '0',
            'borderLeft': 'none',
            'overflow': 'hidden'
        },
        'functional-close-button': {
            'position': 'absolute',
            'left': '-40px',
            'top': '10px',
            'backgroundColor': '#6a0dad',
            'border': 'none',
            'color': 'white',
            'borderRadius': '5px',
            'width': '30px',
            'height': '30px',
            'cursor': 'pointer',
            'zIndex': 101,
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center'
        },
        'functional-header': {
            'color': '#b19cd9',
            'marginBottom': '20px',
            'paddingBottom': '10px',
            'borderBottom': '1px solid #444'
        },
        'functional-content': {
            'flexGrow': 1,
            'color': 'white'
        }
    }
    
    return html.Div([
        dbc.Button(
            html.I(className="fas fa-times"),
            id='functional-close-button',
            style=styles['functional-close-button']
        ),
        html.Div(id='functional-content', style=styles['functional-content'])
    ], id='functional-view', style=styles['functional-view'])

def create_diagnostico_content():
    """Contenido para la funcionalidad de diagnóstico"""
    return html.Div([
        html.H4("Diagnóstico Médico", style={'color': '#b19cd9', 'marginBottom': '20px'}),
        html.P("Aquí aparecerá el análisis detallado de tus síntomas."),
        dbc.Card([
            dbc.CardBody([
                html.H6("Síntomas analizados", style={'color': '#b19cd9'}),
                html.Ul([
                    html.Li("Dolor de cabeza"),
                    html.Li("Fiebre"),
                    html.Li("Fatiga")
                ])
            ])
        ], style={'backgroundColor': '#2a2a4a', 'border': 'none', 'marginBottom': '15px'}),
        dbc.Card([
            dbc.CardBody([
                html.H6("Posibles diagnósticos", style={'color': '#b19cd9'}),
                html.Ul([
                    html.Li("Resfriado común"),
                    html.Li("Gripe"),
                    html.Li("Migraña")
                ])
            ])
        ], style={'backgroundColor': '#2a2a4a', 'border': 'none'})
    ])

def create_explicacion_content():
    """Contenido para la funcionalidad de explicación médica"""
    return html.Div([
        html.H4("Explicación Médica", style={'color': '#b19cd9', 'marginBottom': '20px'}),
        html.P("Aquí aparecerán las explicaciones detalladas de términos médicos."),
        dbc.Card([
            dbc.CardBody([
                html.H6("Términos explicados", style={'color': '#b19cd9'}),
                html.Div([
                    html.Strong("Hipertensión: "),
                    html.Span("Presión arterial elevada de forma crónica")
                ]),
                html.Br(),
                html.Div([
                    html.Strong("Diabetes: "),
                    html.Span("Enfermedad metabólica caracterizada por niveles altos de glucosa")
                ])
            ])
        ], style={'backgroundColor': '#2a2a4a', 'border': 'none'})
    ]) 