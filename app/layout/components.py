import dash_bootstrap_components as dbc
from dash import html
from app.app_config import COLORS

def create_header():
    """Crea el header de la aplicación"""
    return dbc.Navbar([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-heartbeat", style={'fontSize': '2rem', 'color': COLORS['accent'], 'marginRight': '10px'}),
                        html.H3("Asistente Médico Rural", className="mb-0", style={'color': COLORS['primary'], 'fontWeight': 'bold'})
                    ], style={'display': 'flex', 'alignItems': 'center'})
                ], width=8),
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-map-marker-alt", style={'marginRight': '5px'}),
                        html.Span("Antioquia, Colombia", style={'fontSize': '0.9rem'})
                    ], style={'textAlign': 'right', 'color': COLORS['text']})
                ], width=4)
            ], align="center")
        ], fluid=True)
    ], color=COLORS['white'], className="mb-4 shadow-sm")

def create_function_card(title, description, icon, color, card_id):
    """Crea una tarjeta de funcionalidad"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Div([
                    html.I(className=f"fas {icon}", style={
                        'fontSize': '3rem', 
                        'color': color, 
                        'marginBottom': '20px',
                        'textShadow': '0 2px 4px rgba(0,0,0,0.1)'
                    }),
                ], style={'marginBottom': '15px'}),
                html.H5(title, className="card-title", style={
                    'color': COLORS['dark_blue'], 
                    'fontWeight': 'bold',
                    'marginBottom': '15px'
                }),
                html.P(description, className="card-text", style={
                    'color': COLORS['text'], 
                    'fontSize': '0.95rem',
                    'lineHeight': '1.5',
                    'marginBottom': '20px'
                }),
                dbc.Button("Usar Función", 
                          color="primary", 
                          size="sm", 
                          id=card_id, 
                          className="mt-auto",
                          style={
                              'borderRadius': '25px',
                              'fontWeight': 'bold',
                              'textTransform': 'uppercase',
                              'fontSize': '0.8rem',
                              'padding': '8px 20px'
                          })
            ], style={'textAlign': 'center', 'height': '100%', 'display': 'flex', 'flexDirection': 'column'})
        ])
    ], className="h-100 shadow-sm card-hover", style={
        'borderLeft': f'5px solid {color}',
        'background': f'linear-gradient(135deg, {COLORS["white"]} 0%, {COLORS["light_blue"]} 100%)',
        'borderRadius': '12px',
        'transition': 'all 0.3s ease'
    })

def mostrar_advertencia_etica():
    """Crea el componente de advertencia ética"""
    return dbc.Alert([
        html.H5([
            html.I(className="fas fa-exclamation-triangle me-2"),
            "⚠️ Advertencia Importante"
        ], style={'color': COLORS['warning']}),
        html.P([
            "Este sistema es una herramienta de apoyo y no reemplaza la consulta médica profesional. ",
            html.Strong("Siempre consulta con un médico calificado para obtener un diagnóstico definitivo."),
            " Los resultados proporcionados son informativos y preliminares."
        ], style={'marginBottom': '10px'}),
        html.Small([
            "El sistema está diseñado para asistir en zonas rurales con acceso limitado a servicios médicos. ",
            "En caso de emergencia, contacta inmediatamente a los servicios de emergencia locales."
        ], style={'color': '#666'})
    ], color="warning", className="mb-4", style={'borderRadius': '8px'}) 