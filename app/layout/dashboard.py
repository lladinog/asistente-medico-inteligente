import dash_bootstrap_components as dbc
from dash import html, dcc
from app.app_config import COLORS
from app.layout.components import create_header, create_function_card

def create_main_layout():
    """Crea el layout principal de la aplicación"""
    return dbc.Container([
        create_header(),
        
        # Sección principal
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2("🩺 Atención Médica al Alcance de tu Comunidad", 
                           style={'color': COLORS['primary'], 'textAlign': 'center', 'marginBottom': '20px'}),
                    html.P("Sistema inteligente diseñado para brindar asistencia médica preliminar a comunidades rurales de Colombia. "
                          "Describe tus síntomas, sube imágenes médicas y recibe orientación profesional.",
                          style={'textAlign': 'center', 'fontSize': '1.1rem', 'color': COLORS['text'], 'marginBottom': '30px'})
                ])
            ], width=12)
        ]),
        
        # Tarjetas de funcionalidades
        dbc.Row([
            dbc.Col([
                create_function_card(
                    "Diagnóstico por Síntomas", 
                    "Describe tus síntomas y recibe un diagnóstico preliminar con recomendaciones",
                    "fa-stethoscope", 
                    COLORS['primary'],
                    "btn-diagnostico"
                )
            ], width=4, className="mb-4"),
            dbc.Col([
                create_function_card(
                    "Análisis de Imágenes", 
                    "Sube radiografías o fotos de lesiones para análisis con IA",
                    "fa-x-ray", 
                    "#FF8C00",
                    "btn-imagenes"
                )
            ], width=4, className="mb-4"),
            dbc.Col([
                create_function_card(
                    "Interpretación de Exámenes", 
                    "Analiza resultados de laboratorio y exámenes médicos",
                    "fa-file-medical", 
                    "#8A2BE2",
                    "btn-examenes"
                )
            ], width=4, className="mb-4"),
        ]),
        
        dbc.Row([
            dbc.Col([
                create_function_card(
                    "Explicación Médica", 
                    "Convierte términos médicos complejos en lenguaje sencillo",
                    "fa-comment-medical", 
                    "#20B2AA",
                    "btn-explicacion"
                )
            ], width=4, className="mb-4"),
            dbc.Col([
                create_function_card(
                    "Centros Médicos Cercanos", 
                    "Encuentra el centro de salud más cercano a tu ubicación",
                    "fa-hospital", 
                    "#32CD32",
                    "btn-centros"
                )
            ], width=4, className="mb-4"),
            dbc.Col([
                create_function_card(
                    "Resumen Médico", 
                    "Genera un reporte completo para tu médico de familia",
                    "fa-file-medical-alt", 
                    "#FF69B4",
                    "btn-resumen"
                )
            ], width=4, className="mb-4"),
        ]),
        
        # Modal dinámico para cada funcionalidad
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
            dbc.ModalBody(id="modal-body"),
            dbc.ModalFooter([
                dbc.Button("Cerrar", id="close-modal", className="ms-auto", n_clicks=0)
            ])
        ], id="main-modal", is_open=False, size="xl"),
        
        # Sección de información del sistema médico
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H4([
                                html.I(className="fas fa-brain me-2"),
                                "Sistema de Diagnóstico Médico Avanzado"
                            ], style={'color': COLORS['primary'], 'textAlign': 'center', 'marginBottom': '15px'}),
                            html.P([
                                "Nuestro sistema utiliza inteligencia artificial y una base de conocimiento médico completa ",
                                "para proporcionar diagnósticos preliminares precisos y recomendaciones personalizadas. ",
                                "Diseñado específicamente para comunidades rurales con acceso limitado a servicios médicos."
                            ], style={'textAlign': 'center', 'fontSize': '1rem', 'color': COLORS['text'], 'marginBottom': '20px'}),
                            dbc.Button([
                                html.I(className="fas fa-info-circle me-2"),
                                "Conocer Más Sobre el Sistema"
                            ], color="info", size="lg", id="btn-info-sistema", 
                            style={'borderRadius': '25px', 'fontWeight': 'bold'})
                        ], style={'textAlign': 'center'})
                    ])
                ], style={'backgroundColor': COLORS['light_blue'], 'borderRadius': '15px'})
            ], width=12, className="mb-4")
        ]),
        
        # Contenedor para información del sistema
        html.Div(id="sistema-medico-info"),
        
        # Footer
        html.Hr(style={'marginTop': '50px'}),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P("⚠️ Este sistema proporciona información médica preliminar y no reemplaza la consulta con un profesional de la salud.", 
                          className="text-center", style={'color': COLORS['accent'], 'fontWeight': 'bold', 'fontSize': '0.9rem'}),
                    html.P("🏥 Desarrollado para mejorar el acceso a servicios de salud en zonas rurales de Colombia", 
                          className="text-center", style={'color': COLORS['text'], 'fontSize': '0.8rem'})
                ])
            ], width=12)
        ], className="mb-4")
        
    ], fluid=True, style={'backgroundColor': COLORS['background'], 'minHeight': '100vh'})
