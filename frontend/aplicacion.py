import dash
from dash import dcc, html, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import base64
import io
from datetime import datetime
import json

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Asistente Médico Rural"

# Datos mockeados para centros médicos
CENTROS_MEDICOS = {
    "Antioquia": [
        {"nombre": "Hospital San Rafael", "municipio": "Medellín", "direccion": "Calle 50 #30-20", "telefono": "604-555-0123", "distancia": "15 km", "especialidades": ["Medicina General", "Urgencias", "Pediatría"]},
        {"nombre": "Centro de Salud La Paz", "municipio": "Bello", "direccion": "Carrera 20 #45-30", "telefono": "604-555-0456", "distancia": "8 km", "especialidades": ["Medicina General", "Ginecología"]},
        {"nombre": "Puesto de Salud Rural", "municipio": "Barbosa", "direccion": "Vereda El Progreso", "telefono": "604-555-0789", "distancia": "5 km", "especialidades": ["Medicina General"]},
    ],
    "Cundinamarca": [
        {"nombre": "Hospital Central", "municipio": "Bogotá", "direccion": "Avenida 68 #40-50", "telefono": "601-555-0321", "distancia": "25 km", "especialidades": ["Medicina General", "Urgencias", "Cardiología"]},
        {"nombre": "Centro de Salud Suba", "municipio": "Bogotá", "direccion": "Calle 145 #91-20", "telefono": "601-555-0654", "distancia": "12 km", "especialidades": ["Medicina General", "Pediatría"]},
    ]
}

# Datos mockeados para médicos
MEDICOS_ASIGNADOS = [
    {"nombre": "Dr. Carlos Mendoza", "especialidad": "Medicina General", "centro": "Hospital San Rafael", "disponibilidad": "Lunes a Viernes 8:00-16:00"},
    {"nombre": "Dra. Ana María López", "especialidad": "Pediatría", "centro": "Centro de Salud La Paz", "disponibilidad": "Martes y Jueves 9:00-13:00"},
    {"nombre": "Dr. Roberto Silva", "especialidad": "Medicina Rural", "centro": "Puesto de Salud Rural", "disponibilidad": "Lunes, Miércoles y Viernes 7:00-15:00"},
]

# Estilos personalizados
COLORS = {
    'primary': '#0066CC',      
    'secondary': '#4A90E2',    
    'accent': '#FF6B6B',       
    'success': '#28A745',     
    'warning': '#FFC107',     
    'info': '#17A2B8',       
    'background': '#F8FBFF', 
    'text': '#2C3E50',
    'white': '#FFFFFF',
    'light_blue': '#E3F2FD',  
    'dark_blue': '#003D82'  
}

COORDENADAS_CENTROS = {
    "Antioquia": [
        {"nombre": "Hospital San Rafael", "lat": 6.2476, "lng": -75.5658, "municipio": "Medellín"},
        {"nombre": "Centro de Salud La Paz", "lat": 6.3369, "lng": -75.5542, "municipio": "Bello"},
        {"nombre": "Puesto de Salud Rural", "lat": 6.4395, "lng": -75.6207, "municipio": "Barbosa"},
    ],
    "Cundinamarca": [
        {"nombre": "Hospital Central", "lat": 4.6097, "lng": -74.0817, "municipio": "Bogotá"},
        {"nombre": "Centro de Salud Suba", "lat": 4.7570, "lng": -74.0814, "municipio": "Bogotá"},
    ]
}

# Componentes
def create_header():
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
    ], color=COLORS['white'], light=True, className="mb-4 shadow-sm")

def create_function_card(title, description, icon, color, card_id):
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

# Layout principal
app.layout = dbc.Container([
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

# Callbacks para manejar los modales
@app.callback(
    [Output("main-modal", "is_open"),
     Output("modal-title", "children"),
     Output("modal-body", "children")],
    [Input("btn-diagnostico", "n_clicks"),
     Input("btn-imagenes", "n_clicks"),
     Input("btn-examenes", "n_clicks"),
     Input("btn-explicacion", "n_clicks"),
     Input("btn-centros", "n_clicks"),
     Input("btn-resumen", "n_clicks"),
     Input("close-modal", "n_clicks")],
    [State("main-modal", "is_open")]
)
def toggle_modal(n1, n2, n3, n4, n5, n6, n_close, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, "", ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "close-modal":
        return False, "", ""
    
    # Contenido específico para cada modal
    if button_id == "btn-diagnostico":
        return True, "🧠 Diagnóstico por Síntomas", create_diagnostico_content()
    elif button_id == "btn-imagenes":
        return True, "🩻 Análisis de Imágenes Médicas", create_imagenes_content()
    elif button_id == "btn-examenes":
        return True, "📄 Interpretación de Exámenes", create_examenes_content()
    elif button_id == "btn-explicacion":
        return True, "🗣️ Explicación Médica", create_explicacion_content()
    elif button_id == "btn-centros":
        return True, "📍 Centros Médicos Cercanos", create_centros_content()
    elif button_id == "btn-resumen":
        return True, "📬 Resumen Médico", create_resumen_content()
    
    return False, "", ""

def create_diagnostico_content():
    return html.Div([
        dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            "Describe tus síntomas con el mayor detalle posible. Este diagnóstico es preliminar y no reemplaza una consulta médica."
        ], color="info", className="mb-3"),
        
        dbc.Form([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Edad", html_for="edad-input"),
                    dbc.Input(id="edad-input", type="number", placeholder="Ej: 35", min=1, max=120)
                ], width=6),
                dbc.Col([
                    dbc.Label("Sexo", html_for="sexo-select"),
                    dbc.Select(id="sexo-select", options=[
                        {"label": "Masculino", "value": "M"},
                        {"label": "Femenino", "value": "F"},
                        {"label": "Prefiero no decir", "value": "N"}
                    ])
                ], width=6)
            ], className="mb-3"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Label("Describe tus síntomas principales", html_for="sintomas-textarea"),
                    dbc.Textarea(id="sintomas-textarea", 
                               placeholder="Ej: Tengo dolor de cabeza fuerte desde hace 2 días, fiebre de 38°C, y me duele la garganta al tragar...",
                               rows=4, className="mb-3")
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Label("¿Cuánto tiempo llevas con estos síntomas?", html_for="tiempo-select"),
                    dbc.Select(id="tiempo-select", options=[
                        {"label": "Menos de 24 horas", "value": "24h"},
                        {"label": "1-3 días", "value": "3d"},
                        {"label": "1 semana", "value": "1w"},
                        {"label": "Más de 1 semana", "value": "1w+"}
                    ])
                ], width=6),
                dbc.Col([
                    dbc.Label("Intensidad del malestar (1-10)", html_for="intensidad-slider"),
                    dcc.Slider(id="intensidad-slider", min=1, max=10, step=1, value=5, 
                             marks={i: str(i) for i in range(1, 11)})
                ], width=6)
            ], className="mb-3"),
            
            dbc.Button("Analizar Síntomas", color="primary", size="lg", className="w-100", id="btn-analizar-sintomas"),
            
            html.Div(id="resultado-diagnostico", className="mt-4")
        ])
    ])

def create_imagenes_content():
    return html.Div([
        dbc.Alert([
            html.I(className="fas fa-camera me-2"),
            "Sube una imagen médica (radiografía, foto de lesión, etc.) para análisis con inteligencia artificial."
        ], color="info", className="mb-3"),
        
        dbc.Form([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Tipo de imagen médica", html_for="tipo-imagen-select"),
                    dbc.Select(id="tipo-imagen-select", options=[
                        {"label": "Radiografía de tórax", "value": "rx_torax"},
                        {"label": "Radiografía de extremidades", "value": "rx_extremidades"},
                        {"label": "Lesión en piel", "value": "lesion_piel"},
                        {"label": "Examen de laboratorio", "value": "lab"},
                        {"label": "Otro", "value": "otro"}
                    ])
                ], width=12, className="mb-3")
            ]),
            
            dbc.Row([
                dbc.Col([
                    dcc.Upload(
                        id='upload-imagen',
                        children=html.Div([
                            html.I(className="fas fa-cloud-upload-alt", style={'fontSize': '3rem', 'color': COLORS['primary']}),
                            html.Br(),
                            html.P('Arrastra la imagen aquí o haz clic para seleccionar', style={'margin': '10px'})
                        ]),
                        style={
                            'width': '100%', 'height': '200px', 'lineHeight': '200px',
                            'borderWidth': '2px', 'borderStyle': 'dashed', 'borderRadius': '10px',
                            'textAlign': 'center', 'backgroundColor': '#f8f9fa',
                            'borderColor': COLORS['primary']
                        },
                        multiple=False
                    )
                ], width=12, className="mb-3")
            ]),
            
            html.Div(id="preview-imagen", className="mb-3"),
            
            dbc.Button("Analizar Imagen", color="primary", size="lg", className="w-100", id="btn-analizar-imagen"),
            
            html.Div(id="resultado-imagen", className="mt-4")
        ])
    ])

def create_examenes_content():
    return html.Div([
        dbc.Alert([
            html.I(className="fas fa-file-pdf me-2"),
            "Sube un archivo PDF o imagen de tus exámenes de laboratorio para interpretación automática."
        ], color="info", className="mb-3"),
        
        dbc.Form([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Tipo de examen", html_for="tipo-examen-select"),
                    dbc.Select(id="tipo-examen-select", options=[
                        {"label": "Hemograma completo", "value": "hemograma"},
                        {"label": "Perfil lipídico", "value": "lipidos"},
                        {"label": "Glucemia", "value": "glucosa"},
                        {"label": "Función renal", "value": "renal"},
                        {"label": "Función hepática", "value": "hepatico"},
                        {"label": "Otro", "value": "otro"}
                    ])
                ], width=12, className="mb-3")
            ]),
            
            dbc.Row([
                dbc.Col([
                    dcc.Upload(
                        id='upload-examen',
                        children=html.Div([
                            html.I(className="fas fa-file-upload", style={'fontSize': '3rem', 'color': '#8A2BE2'}),
                            html.Br(),
                            html.P('Arrastra el archivo aquí o haz clic para seleccionar', style={'margin': '10px'}),
                            html.Small('Formatos: PDF, JPG, PNG', style={'color': '#666'})
                        ]),
                        style={
                            'width': '100%', 'height': '200px', 'lineHeight': '180px',
                            'borderWidth': '2px', 'borderStyle': 'dashed', 'borderRadius': '10px',
                            'textAlign': 'center', 'backgroundColor': '#f8f9fa',
                            'borderColor': '#8A2BE2'
                        },
                        multiple=False
                    )
                ], width=12, className="mb-3")
            ]),
            
            html.Div(id="preview-examen", className="mb-3"),
            
            dbc.Button("Interpretar Examen", color="secondary", size="lg", className="w-100", id="btn-interpretar-examen"),
            
            html.Div(id="resultado-examen", className="mt-4")
        ])
    ])

def create_explicacion_content():
    return html.Div([
        dbc.Alert([
            html.I(className="fas fa-language me-2"),
            "Ingresa términos médicos complejos y recibe explicaciones en lenguaje claro y comprensible."
        ], color="info", className="mb-3"),
        
        dbc.Form([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Término médico a explicar", html_for="termino-input"),
                    dbc.Input(id="termino-input", 
                             placeholder="Ej: hipertensión, diabetes, neumonía, arritmia...",
                             className="mb-3")
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Label("Nivel de explicación", html_for="nivel-explicacion"),
                    dbc.RadioItems(
                        id="nivel-explicacion",
                        options=[
                            {"label": "Muy simple (para niños)", "value": "simple"},
                            {"label": "Intermedio (adultos)", "value": "intermedio"},
                            {"label": "Detallado (con terminología)", "value": "detallado"}
                        ],
                        value="intermedio",
                        className="mb-3"
                    )
                ], width=12)
            ]),
            
            dbc.Button("Explicar Término", color="info", size="lg", className="w-100", id="btn-explicar-termino"),
            
            html.Div(id="resultado-explicacion", className="mt-4")
        ])
    ])

def create_centros_content():
    return html.Div([
        dbc.Alert([
            html.I(className="fas fa-map-marker-alt me-2"),
            "Encuentra centros de salud cercanos con mapa interactivo y contacto directo con médicos disponibles."
        ], color="info", className="mb-3"),
        
        dbc.Form([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Departamento", html_for="departamento-select"),
                    dbc.Select(id="departamento-select", 
                             options=[
                                 {"label": "Antioquia", "value": "Antioquia"},
                                 {"label": "Cundinamarca", "value": "Cundinamarca"},
                                 {"label": "Valle del Cauca", "value": "Valle"},
                                 {"label": "Santander", "value": "Santander"}
                             ],
                             value="Antioquia")
                ], width=6),
                dbc.Col([
                    dbc.Label("Especialidad requerida", html_for="especialidad-select"),
                    dbc.Select(id="especialidad-select",
                             options=[
                                 {"label": "Cualquiera", "value": "todas"},
                                 {"label": "Medicina General", "value": "Medicina General"},
                                 {"label": "Urgencias", "value": "Urgencias"},
                                 {"label": "Pediatría", "value": "Pediatría"},
                                 {"label": "Ginecología", "value": "Ginecología"}
                             ],
                             value="todas")
                ], width=6)
            ], className="mb-3"),
            
            dbc.Button("🔍 Buscar Centros", color="primary", size="lg", className="w-100 mb-3", 
                      id="btn-buscar-centros", style={'borderRadius': '25px', 'fontWeight': 'bold'}),
            
            # Contenedor para el mapa
            html.Div(id="mapa-centros", className="mb-3"),
            
            html.Div(id="resultado-centros")
        ])
    ])

def create_resumen_content():
    return html.Div([
        dbc.Alert([
            html.I(className="fas fa-user-md me-2"),
            "Genera un resumen médico y conéctate directamente con el médico más cercano disponible."
        ], color="info", className="mb-3"),
        
        dbc.Tabs([
            dbc.Tab(label="📋 Crear Resumen", tab_id="tab-resumen"),
            dbc.Tab(label="👨‍⚕️ Contactar Médico", tab_id="tab-contacto"),
            dbc.Tab(label="📱 Estado de Envío", tab_id="tab-estado")
        ], id="tabs-resumen", active_tab="tab-resumen"),
        
        html.Div(id="content-tabs-resumen", className="mt-3")
    ])

# Callback para búsqueda de centros médicos
@app.callback(
    [Output("resultado-centros", "children"),
     Output("mapa-centros", "children")],
    Input("btn-buscar-centros", "n_clicks"),
    [State("departamento-select", "value"),
     State("especialidad-select", "value")]
)
def buscar_centros_con_mapa(n_clicks, departamento, especialidad):
    if not n_clicks:
        return "", ""
    
    centros = CENTROS_MEDICOS.get(departamento, [])
    coordenadas = COORDENADAS_CENTROS.get(departamento, [])
    
    # Filtrar por especialidad
    if especialidad != "todas":
        centros = [centro for centro in centros if especialidad in centro["especialidades"]]
        coordenadas = [coord for coord in coordenadas 
                      if any(c["nombre"] == coord["nombre"] for c in centros)]
    
    if not centros:
        return dbc.Alert("No se encontraron centros médicos con los criterios especificados.", color="warning"), ""
    
    # Crear mapa
    mapa_html = f"""
    <div id="mapa-leaflet" style="height: 400px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.css" />
    <script>
        setTimeout(function() {{
            if (typeof L !== 'undefined') {{
                var map = L.map('mapa-leaflet').setView([{coordenadas[0]["lat"]}, {coordenadas[0]["lng"]}], 11);
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '© OpenStreetMap contributors'
                }}).addTo(map);
                
                var markers = [];
                {chr(10).join([f"""
                var marker{i} = L.marker([{coord["lat"]}, {coord["lng"]}])
                    .addTo(map)
                    .bindPopup('<b>{coord["nombre"]}</b><br>{coord["municipio"]}<br><button onclick="contactarCentro({i})" class="btn btn-sm btn-primary">Contactar</button>');
                markers.push(marker{i});
                """ for i, coord in enumerate(coordenadas)])}
                
                window.contactarCentro = function(index) {{
                    document.getElementById('centro-' + index).scrollIntoView({{behavior: 'smooth'}});
                    document.getElementById('centro-' + index).style.border = '3px solid #0066CC';
                }};
            }}
        }}, 500);
    </script>
    """
    
    mapa_component = html.Div([
        html.H5("🗺️ Ubicación de Centros Médicos", style={'color': COLORS['primary'], 'marginBottom': '15px'}),
        html.Div([
            html.Iframe(srcDoc=mapa_html, style={'width': '100%', 'height': '450px', 'border': 'none'})
        ])
    ])
    
    # Crear cards para centros
    cards = []
    for i, centro in enumerate(centros):
        medico_disponible = next((m for m in MEDICOS_ASIGNADOS if centro["nombre"] in m["centro"]), MEDICOS_ASIGNADOS[0])
        
        card = dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H5([
                        html.I(className="fas fa-hospital me-2", style={'color': COLORS['primary']}),
                        centro['nombre']
                    ], className="card-title", style={'color': COLORS['primary'], 'borderBottom': '2px solid #eee', 'paddingBottom': '10px'}),
                    
                    dbc.Row([
                        dbc.Col([
                            html.P([
                                html.I(className="fas fa-map-marker-alt me-2", style={'color': COLORS['info']}),
                                html.Strong("Ubicación: "), f"{centro['direccion']}, {centro['municipio']}", html.Br(),
                                html.I(className="fas fa-phone me-2", style={'color': COLORS['success']}),
                                html.Strong("Teléfono: "), centro['telefono'], html.Br(),
                                html.I(className="fas fa-route me-2", style={'color': COLORS['warning']}),
                                html.Strong("Distancia: "), centro['distancia'], html.Br(),
                                html.I(className="fas fa-user-md me-2", style={'color': COLORS['primary']}),
                                html.Strong("Especialidades: "), ", ".join(centro['especialidades'])
                            ], style={'marginBottom': '15px'})
                        ], width=8),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H6("👨‍⚕️ Médico Disponible", style={'color': COLORS['success'], 'fontSize': '0.9rem'}),
                                    html.P([
                                        html.Strong(medico_disponible['nombre']), html.Br(),
                                        html.Small(medico_disponible['especialidad']), html.Br(),
                                        html.Small(medico_disponible['disponibilidad'], style={'color': COLORS['info']})
                                    ], style={'fontSize': '0.8rem', 'marginBottom': '10px'}),
                                    dbc.Badge("Disponible Ahora", color="success", className="mb-2")
                                ])
                            ], style={'backgroundColor': COLORS['light_blue']})
                        ], width=4)
                    ]),
                    
                    html.Div([
                        dbc.Button([
                            html.I(className="fas fa-video me-2"),
                            "Teleconsulta"
                        ], color="primary", size="sm", className="me-2", id=f"btn-teleconsulta-{i}"),
                        dbc.Button([
                            html.I(className="fas fa-envelope me-2"),
                            "Enviar Caso"
                        ], color="success", size="sm", className="me-2", id=f"btn-enviar-caso-{i}"),
                        dbc.Button([
                            html.I(className="fas fa-phone me-2"),
                            "Llamar"
                        ], color="info", size="sm", className="me-2", id=f"btn-llamar-{i}"),
                        dbc.Button([
                            html.I(className="fas fa-map me-2"),
                            "Ver en Mapa"
                        ], color="outline-primary", size="sm", id=f"btn-mapa-{i}")
                    ], style={'textAlign': 'center', 'marginTop': '15px'})
                ])
            ])
        ], className="mb-3 shadow-sm", style={'borderRadius': '12px', 'border': '1px solid #e3f2fd'}, id=f"centro-{i}")
        cards.append(card)
    
    resultado = html.Div([
        html.H5(f"🏥 {len(centros)} centros médicos encontrados en {departamento}:", 
               className="mb-3", style={'color': COLORS['primary']}),
        html.Div(cards)
    ])
    
    return resultado, mapa_component

# Callback para simulación de contacto con médico 
@app.callback(
    [Output("resultado-resumen", "children"),
     Output("tabs-resumen", "active_tab"),
     Output("medico-seleccionado-info", "children")],
    Input("btn-crear-resumen", "n_clicks"),
    [State("nombre-paciente", "value"),
     State("cedula-paciente", "value"),
     State("edad-paciente", "value"),
     State("telefono-paciente", "value"),
     State("motivo-consulta", "value"),
     State("sintomas-actuales", "value"),
     State("prioridad-caso", "value")]
)
def generar_resumen(n_clicks, nombre, cedula, edad, resumen, medico_idx):
    if not n_clicks:
        return ""
    
    if not all([nombre, cedula, edad, resumen]):
        return dbc.Alert("Por favor completa todos los campos requeridos.", color="danger")
    
    medico = MEDICOS_ASIGNADOS[int(medico_idx)] if medico_idx is not None else MEDICOS_ASIGNADOS[0]
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    resumen_html = dbc.Card([
        dbc.CardHeader([
            html.H4("📋 Resumen Médico Generado", className="mb-0", style={'color': COLORS['primary']})
        ]),
        dbc.CardBody([
            html.Div([
                html.H6("INFORMACIÓN DEL PACIENTE", style={'color': COLORS['primary'], 'borderBottom': '2px solid #eee', 'paddingBottom': '5px'}),
                html.P([
                    html.Strong("Nombre: "), nombre, html.Br(),
                    html.Strong("Cédula: "), cedula, html.Br(),
                    html.Strong("Edad: "), f"{edad} años", html.Br(),
                    html.Strong("Fecha de consulta: "), fecha_actual
                ], className="mb-3"),
                
                html.H6("MOTIVO DE CONSULTA", style={'color': COLORS['primary'], 'borderBottom': '2px solid #eee', 'paddingBottom': '5px'}),
                html.P(resumen, className="mb-3"),
                
                html.H6("MÉDICO DESTINATARIO", style={'color': COLORS['primary'], 'borderBottom': '2px solid #eee', 'paddingBottom': '5px'}),
                html.P([
                    html.Strong("Nombre: "), medico['nombre'], html.Br(),
                    html.Strong("Especialidad: "), medico['especialidad'], html.Br(),
                    html.Strong("Centro: "), medico['centro'], html.Br(),
                    html.Strong("Disponibilidad: "), medico['disponibilidad']
                ], className="mb-3"),
                
                dbc.Alert([
                    html.I(className="fas fa-paper-plane me-2"),
                    f"✅ Resumen enviado exitosamente a {medico['nombre']} en {medico['centro']}",
                    html.Br(),
                    html.Small(f"Fecha de envío: {fecha_actual}")
                ], color="success", className="mb-3"),
                
                html.Div([
                    dbc.Button("📧 Enviar por Email", color="primary", size="sm", className="me-2"),
                    dbc.Button("📱 Enviar por WhatsApp", color="success", size="sm", className="me-2"),
                    dbc.Button("📄 Descargar PDF", color="secondary", size="sm")
                ], style={'textAlign': 'center'})
            ])
        ])
    ], className="mt-3")
    
    return resumen_html

# Callback para agente de ética y advertencias
def mostrar_advertencia_etica():
    return dbc.Alert([
        html.Div([
            html.I(className="fas fa-exclamation-triangle", style={'fontSize': '1.5rem', 'marginRight': '10px'}),
            html.Div([
                html.H6("⚠️ ADVERTENCIA IMPORTANTE", className="mb-2", style={'color': '#721c24'}),
                html.P([
                    "• Este sistema proporciona información médica preliminar y orientativa.", html.Br(),
                    "• NO reemplaza el diagnóstico ni tratamiento de un profesional de la salud.", html.Br(),
                    "• En caso de emergencia médica, dirígete inmediatamente al centro de salud más cercano.", html.Br(),
                    "• Siempre consulta con un médico antes de tomar decisiones sobre tu salud."
                ], className="mb-0", style={'fontSize': '0.9rem'})
            ])
        ], style={'display': 'flex', 'alignItems': 'flex-start'})
    ], color="danger", className="mb-3")

# Callbacks para las funcionalidades que requieren integración posterior
@app.callback(
    Output("resultado-diagnostico", "children"),
    Input("btn-analizar-sintomas", "n_clicks"),
    [State("edad-input", "value"),
     State("sexo-select", "value"),
     State("sintomas-textarea", "value"),
     State("tiempo-select", "value"),
     State("intensidad-slider", "value")]
)
def analizar_sintomas(n_clicks, edad, sexo, sintomas, tiempo, intensidad):
    if not n_clicks or not sintomas:
        return ""
    
    # Mostrar advertencia ética
    advertencia = mostrar_advertencia_etica()
    
    # Simulación de análisis
    resultado_simulado = dbc.Card([
        dbc.CardHeader([
            html.H5("🧠 Análisis Preliminar de Síntomas", className="mb-0", style={'color': COLORS['primary']})
        ]),
        dbc.CardBody([
            html.Div([
                html.H6("DATOS ANALIZADOS:", style={'color': COLORS['primary']}),
                html.P([
                    f"Edad: {edad} años | Sexo: {sexo} | Intensidad: {intensidad}/10 | Duración: {tiempo}"
                ], style={'backgroundColor': '#f8f9fa', 'padding': '10px', 'borderRadius': '5px'}),
                
                html.H6("SÍNTOMAS REPORTADOS:", style={'color': COLORS['primary']}),
                html.P(sintomas, style={'backgroundColor': '#f8f9fa', 'padding': '10px', 'borderRadius': '5px'}),
                
                html.H6("🔍 DIAGNÓSTICO PRELIMINAR:", style={'color': COLORS['primary']}),
                html.Div([
                    html.P("Basado en los síntomas descritos, las posibles condiciones incluyen:", className="mb-2"),
                    html.Ul([
                        html.Li("Infección viral del tracto respiratorio superior (probabilidad: 65%)"),
                        html.Li("Faringitis bacteriana (probabilidad: 25%)"),
                        html.Li("Otras condiciones a considerar (probabilidad: 10%)")
                    ]),
                    
                    html.H6("💊 RECOMENDACIONES:", style={'color': COLORS['accent']}),
                    html.Ul([
                        html.Li("Mantén reposo e hidratación adecuada"),
                        html.Li("Toma analgésicos de venta libre si es necesario"),
                        html.Li("Consulta a un médico si los síntomas empeoran o persisten más de 5 días"),
                        html.Li("Busca atención médica urgente si tienes dificultad para respirar")
                    ])
                ], style={'backgroundColor': '#e8f5e8', 'padding': '15px', 'borderRadius': '5px'})
            ])
        ])
    ], className="mt-3")
    
    return html.Div([advertencia, resultado_simulado])

@app.callback(
    Output("resultado-imagen", "children"),
    Input("btn-analizar-imagen", "n_clicks"),
    [State("tipo-imagen-select", "value"),
     State("upload-imagen", "contents"),
     State("upload-imagen", "filename")]
)
def analizar_imagen(n_clicks, tipo_imagen, contents, filename):
    if not n_clicks or not contents:
        return ""
    
    advertencia = mostrar_advertencia_etica()
    
    resultado_simulado = dbc.Card([
        dbc.CardHeader([
            html.H5("🩻 Análisis de Imagen Médica", className="mb-0", style={'color': COLORS['primary']})
        ]),
        dbc.CardBody([
            html.Div([
                html.H6("IMAGEN ANALIZADA:", style={'color': COLORS['primary']}),
                html.P([
                    f"Archivo: {filename} | Tipo: {tipo_imagen}"
                ], style={'backgroundColor': '#f8f9fa', 'padding': '10px', 'borderRadius': '5px'}),
                
                html.H6("🔍 HALLAZGOS DEL ANÁLISIS:", style={'color': COLORS['primary']}),
                html.Div([
                    html.P("Procesamiento completado con IA especializada en imágenes médicas:", className="mb-2"),
                    html.Ul([
                        html.Li("✅ Calidad de imagen: Adecuada para análisis"),
                        html.Li("🔍 Estructuras anatómicas: Visibles y bien definidas"),
                        html.Li("⚠️ Hallazgos: Se requiere evaluación profesional"),
                        html.Li("📊 Confianza del análisis: 78%")
                    ]),
                    
                    html.H6("📋 RECOMENDACIONES:", style={'color': COLORS['accent']}),
                    html.P("Este análisis automatizado detectó áreas que requieren atención médica profesional. "
                          "Es fundamental que un radiólogo o médico especialista revise la imagen original "
                          "para un diagnóstico definitivo.", 
                          style={'fontStyle': 'italic', 'color': '#666'})
                ], style={'backgroundColor': '#fff3cd', 'padding': '15px', 'borderRadius': '5px'})
            ])
        ])
    ], className="mt-3")
    
    return html.Div([advertencia, resultado_simulado])

@app.callback(
    Output("resultado-examen", "children"),
    Input("btn-interpretar-examen", "n_clicks"),
    [State("tipo-examen-select", "value"),
     State("upload-examen", "contents"),
     State("upload-examen", "filename")]
)
def interpretar_examen(n_clicks, tipo_examen, contents, filename):
    if not n_clicks or not contents:
        return ""
    
    advertencia = mostrar_advertencia_etica()
    
    # Simulación de interpretación de exámenes 
    resultado_simulado = dbc.Card([
        dbc.CardHeader([
            html.H5("📄 Interpretación de Exámenes", className="mb-0", style={'color': COLORS['primary']})
        ]),
        dbc.CardBody([
            html.Div([
                html.H6("EXAMEN PROCESADO:", style={'color': COLORS['primary']}),
                html.P([
                    f"Archivo: {filename} | Tipo: {tipo_examen}"
                ], style={'backgroundColor': '#f8f9fa', 'padding': '10px', 'borderRadius': '5px'}),
                
                html.H6("📊 VALORES EXTRAÍDOS:", style={'color': COLORS['primary']}),
                html.Div([
                    dbc.Table([
                        html.Thead([
                            html.Tr([
                                html.Th("Parámetro"),
                                html.Th("Valor"),
                                html.Th("Rango Normal"),
                                html.Th("Estado")
                            ])
                        ]),
                        html.Tbody([
                            html.Tr([
                                html.Td("Glucosa"),
                                html.Td("95 mg/dL"),
                                html.Td("70-100 mg/dL"),
                                html.Td(dbc.Badge("Normal", color="success"))
                            ]),
                            html.Tr([
                                html.Td("Colesterol Total"),
                                html.Td("220 mg/dL"),
                                html.Td("< 200 mg/dL"),
                                html.Td(dbc.Badge("Elevado", color="warning"))
                            ]),
                            html.Tr([
                                html.Td("Hemoglobina"),
                                html.Td("13.5 g/dL"),
                                html.Td("12-16 g/dL"),
                                html.Td(dbc.Badge("Normal", color="success"))
                            ])
                        ])
                    ], striped=True, hover=True),
                    
                    html.H6("💡 INTERPRETACIÓN:", style={'color': COLORS['accent']}),
                    html.P("Los resultados muestran valores mayormente normales, con excepción del colesterol "
                          "que se encuentra ligeramente elevado. Se recomienda consulta médica para "
                          "evaluación integral y posibles ajustes en dieta y estilo de vida.")
                ], style={'backgroundColor': '#e7f3ff', 'padding': '15px', 'borderRadius': '5px'})
            ])
        ])
    ], className="mt-3")
    
    return html.Div([advertencia, resultado_simulado])

@app.callback(
    Output("resultado-explicacion", "children"),
    Input("btn-explicar-termino", "n_clicks"),
    [State("termino-input", "value"),
     State("nivel-explicacion", "value")]
)
def explicar_termino(n_clicks, termino, nivel):
    if not n_clicks or not termino:
        return ""
    
    explicaciones = {
        "simple": f"🧒 **{termino.upper()}** explicado para niños:\n\nEs cuando algo en tu cuerpo no está funcionando como debería. Es como cuando un juguete se daña y necesita arreglo.",
        "intermedio": f"👨‍👩‍👧‍👦 **{termino.upper()}** explicado de forma sencilla:\n\nEs una condición médica que afecta el funcionamiento normal del organismo. Puede tener diferentes causas y síntomas que requieren atención médica.",
        "detallado": f"🎓 **{termino.upper()}** explicación técnica:\n\nCondición patológica caracterizada por alteraciones en los procesos fisiológicos normales, con manifestaciones clínicas específicas que requieren evaluación diagnóstica y tratamiento apropiado."
    }
    
    explicacion = explicaciones.get(nivel, explicaciones["intermedio"])
    
    resultado = dbc.Card([
        dbc.CardHeader([
            html.H5("🗣️ Explicación Médica", className="mb-0", style={'color': COLORS['primary']})
        ]),
        dbc.CardBody([
            html.Div([
                html.H6(f"TÉRMINO: {termino.upper()}", style={'color': COLORS['primary']}),
                html.Hr(),
                dcc.Markdown(explicacion, className="mb-3"),
                
                html.H6("📚 INFORMACIÓN ADICIONAL:", style={'color': COLORS['primary']}),
                html.Ul([
                    html.Li("Esta explicación es educativa y no constituye diagnóstico médico"),
                    html.Li("Para información específica sobre tu caso, consulta con un profesional"),
                    html.Li("Si tienes dudas sobre síntomas, busca atención médica apropiada")
                ])
            ])
        ])
    ], className="mt-3")
    
    return resultado

# Callback para preview de imágenes
@app.callback(
    Output("preview-imagen", "children"),
    Input("upload-imagen", "contents"),
    State("upload-imagen", "filename")
)
def preview_imagen(contents, filename):
    if contents is None:
        return ""
    
    return html.Div([
        html.H6("Vista previa de la imagen:", style={'color': COLORS['primary']}),
        html.Img(src=contents, style={'maxWidth': '100%', 'maxHeight': '300px', 'border': '1px solid #ddd', 'borderRadius': '5px'}),
        html.P(f"Archivo: {filename}", style={'fontSize': '0.9rem', 'color': '#666', 'marginTop': '10px'})
    ])

@app.callback(
    Output("preview-examen", "children"),
    Input("upload-examen", "contents"),
    State("upload-examen", "filename")
)
def preview_examen(contents, filename):
    if contents is None:
        return ""
    
    if filename.lower().endswith('.pdf'):
        preview_content = html.Div([
            html.I(className="fas fa-file-pdf", style={'fontSize': '3rem', 'color': '#dc3545'}),
            html.P(f"Archivo PDF: {filename}", style={'marginTop': '10px'})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'})
    else:
        preview_content = html.Div([
            html.Img(src=contents, style={'maxWidth': '100%', 'maxHeight': '300px', 'border': '1px solid #ddd', 'borderRadius': '5px'}),
            html.P(f"Archivo: {filename}", style={'fontSize': '0.9rem', 'color': '#666', 'marginTop': '10px'})
        ])
    
    return html.Div([
        html.H6("Archivo cargado:", style={'color': COLORS['primary']}),
        preview_content
    ])

@app.callback(
    Output("content-tabs-resumen", "children"),
    Input("tabs-resumen", "active_tab")
)
def render_tab_content(active_tab):
    if active_tab == "tab-resumen":
        return crear_tab_resumen()
    elif active_tab == "tab-contacto":
        return crear_tab_contacto()
    elif active_tab == "tab-estado":
        return crear_tab_estado()
    return html.Div()

def crear_tab_resumen():
    return dbc.Form([
        dbc.Row([
            dbc.Col([
                dbc.Label("Información del paciente", style={'fontWeight': 'bold', 'color': COLORS['primary']}),
                dbc.Input(id="nombre-paciente", placeholder="Nombre completo", className="mb-2"),
                dbc.Input(id="cedula-paciente", placeholder="Número de cédula", className="mb-2"),
                dbc.Input(id="edad-paciente", placeholder="Edad", type="number", className="mb-2"),
                dbc.Input(id="telefono-paciente", placeholder="Teléfono de contacto", className="mb-3")
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("Motivo de consulta", style={'fontWeight': 'bold', 'color': COLORS['primary']}),
                dbc.Textarea(id="motivo-consulta", placeholder="Describe el motivo principal de la consulta...", rows=3, className="mb-3")
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("Síntomas actuales", style={'fontWeight': 'bold', 'color': COLORS['primary']}),
                dbc.Textarea(id="sintomas-actuales", placeholder="Lista todos los síntomas que presentas actualmente...", rows=3, className="mb-3")
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("Prioridad del caso", style={'fontWeight': 'bold', 'color': COLORS['primary']}),
                dbc.RadioItems(
                    id="prioridad-caso",
                    options=[
                        {"label": "🟢 Consulta rutinaria", "value": "rutinaria"},
                        {"label": "🟡 Urgencia menor", "value": "menor"},
                        {"label": "🟠 Urgencia mayor", "value": "mayor"},
                        {"label": "🔴 Emergencia", "value": "emergencia"}
                    ],
                    value="rutinaria",
                    className="mb-3"
                )
            ], width=12)
        ]),
        
        dbc.Button([
            html.I(className="fas fa-file-medical me-2"),
            "Crear Resumen y Buscar Médico"
        ], color="primary", size="lg", className="w-100", id="btn-crear-resumen", 
        style={'borderRadius': '25px', 'fontWeight': 'bold'})
    ])

def crear_tab_contacto():
    return html.Div([
        dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            "Selecciona el médico y método de contacto preferido."
        ], color="info", className="mb-3"),
        
        html.Div(id="medico-seleccionado-info", className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("Método de contacto preferido", style={'fontWeight': 'bold', 'color': COLORS['primary']}),
                dbc.Checklist(
                    id="metodos-contacto",
                    options=[
                        {"label": "📧 Correo electrónico", "value": "email"},
                        {"label": "📱 WhatsApp", "value": "whatsapp"},
                        {"label": "📞 Llamada telefónica", "value": "llamada"},
                        {"label": "💬 SMS", "value": "sms"},
                        {"label": "🎥 Videollamada", "value": "video"}
                    ],
                    value=["email"],
                    className="mb-3"
                )
            ], width=12)
        ]),
        
        dbc.Button([
            html.I(className="fas fa-paper-plane me-2"),
            "Enviar Caso al Médico"
        ], color="success", size="lg", className="w-100", id="btn-enviar-medico", 
        style={'borderRadius': '25px', 'fontWeight': 'bold'})
    ])

def crear_tab_estado():
    return html.Div(id="estado-envio-container")

def crear_resumen_y_asignar_medico(n_clicks, nombre, cedula, edad, telefono, motivo, sintomas, prioridad):
    if not n_clicks:
        return "", "tab-resumen", ""
    
    if not all([nombre, cedula, edad, telefono, motivo, sintomas]):
        return dbc.Alert("Por favor completa todos los campos requeridos.", color="danger"), "tab-resumen", ""
    
    # Simular asignación de médico basada en prioridad
    if prioridad == "emergencia":
        medico = {"nombre": "Dr. Emergency Response", "especialidad": "Medicina de Urgencias", 
                 "centro": "Hospital San Rafael", "disponibilidad": "24/7", "tiempo_respuesta": "Inmediato"}
    elif prioridad == "mayor":
        medico = MEDICOS_ASIGNADOS[0]
        medico["tiempo_respuesta"] = "15-30 minutos"
    else:
        medico = MEDICOS_ASIGNADOS[1]
        medico["tiempo_respuesta"] = "1-2 horas"
    
    # Información del médico asignado
    medico_info = dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-user-md me-2"),
                "Médico Asignado"
            ], className="mb-0", style={'color': COLORS['primary']})
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Img(src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxjaXJjbGUgY3g9IjUwIiBjeT0iNTAiIHI9IjUwIiBmaWxsPSIjMDA2NkNDIi8+Cjx0ZXh0IHg9IjUwIiB5PSI1NSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjMwIiBmb250LXdlaWdodD0iYm9sZCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiPkRyPC90ZXh0Pgo8L3N2Zz4K", 
                            style={'width': '80px', 'height': '80px', 'borderRadius': '50%'})
                ], width=3),
                dbc.Col([
                    html.H5(medico['nombre'], style={'color': COLORS['primary']}),
                    html.P([
                        html.Strong("Especialidad: "), medico['especialidad'], html.Br(),
                        html.Strong("Centro: "), medico['centro'], html.Br(),
                        html.Strong("Disponibilidad: "), medico['disponibilidad'], html.Br(),
                        html.Strong("Tiempo de respuesta: "), medico['tiempo_respuesta']
                    ]),
                    dbc.Badge(f"Prioridad: {prioridad.upper()}", 
                            color="danger" if prioridad == "emergencia" else "warning" if prioridad == "mayor" else "success")
                ], width=9)
            ])
        ])
    ], className="mb-3", style={'backgroundColor': COLORS['light_blue']})
    
    return "", "tab-contacto", medico_info

# 9. CALLBACK PARA SIMULAR ENVÍO AL MÉDICO
@app.callback(
    [Output("estado-envio-container", "children"),
     Output("tabs-resumen", "active_tab", allow_duplicate=True)],
    Input("btn-enviar-medico", "n_clicks"),
    State("metodos-contacto", "value"),
    prevent_initial_call=True
)
def simular_envio_medico(n_clicks, metodos):
    if not n_clicks:
        return "", "tab-estado"
    
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Simular estados de envío
    estados_envio = []
    for metodo in metodos:
        if metodo == "email":
            estados_envio.append({
                "metodo": "📧 Correo Electrónico",
                "estado": "Enviado",
                "detalle": "dr.medico@hospital.com",
                "tiempo": fecha_actual,
                "color": "success"
            })
        elif metodo == "whatsapp":
            estados_envio.append({
                "metodo": "📱 WhatsApp",
                "estado": "Entregado",
                "detalle": "+57 300 123 4567",
                "tiempo": fecha_actual,
                "color": "success"
            })
        elif metodo == "llamada":
            estados_envio.append({
                "metodo": "📞 Llamada Programada",
                "estado": "Agendada",
                "detalle": "En 15 minutos",
                "tiempo": fecha_actual,
                "color": "warning"
            })
        elif metodo == "video":
            estados_envio.append({
                "metodo": "🎥 Videollamada",
                "estado": "Link Enviado",
                "detalle": "meet.hospital.com/sala123",
                "tiempo": fecha_actual,
                "color": "info"
            })
    
    # Crear interfaz de seguimiento
    seguimiento = html.Div([
        dbc.Alert([
            html.I(className="fas fa-check-circle me-2"),
            "¡Caso enviado exitosamente al médico asignado!"
        ], color="success", className="mb-3"),
        
        html.H5("📊 Estado del Envío", style={'color': COLORS['primary'], 'marginBottom': '20px'}),
        
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        dbc.Badge(estado["metodo"], color=estado["color"], className="me-2 mb-2"),
                        html.Strong(f"Estado: {estado['estado']}", style={'color': COLORS['primary']}),
                        html.Br(),
                        html.Small(f"Detalle: {estado['detalle']}"),
                        html.Br(),
                        html.Small(f"Hora: {estado['tiempo']}", style={'color': '#666'})
                    ])
                ])
            ], className="mb-2", style={'backgroundColor': COLORS['light_blue']})
            for estado in estados_envio
        ]),
        
        html.Hr(),
        
        html.Div([
            html.H6("🕐 Próximos Pasos:", style={'color': COLORS['primary']}),
            html.Ul([
                html.Li("El médico revisará tu caso en los próximos minutos"),
                html.Li("Recibirás una respuesta según el método de contacto seleccionado"),
                html.Li("Mantén tu teléfono disponible para posibles llamadas"),
                html.Li("Revisa tu correo electrónico regularmente")
            ])
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Button([
                    html.I(className="fas fa-download me-2"),
                    "Descargar Resumen PDF"
                ], color="secondary", className="w-100 mb-2")
            ], width=6),
            dbc.Col([
                dbc.Button([
                    html.I(className="fas fa-share me-2"),
                    "Compartir Caso"
                ], color="info", className="w-100 mb-2")
            ], width=6)
        ]),
        
        dbc.Alert([
            html.I(className="fas fa-clock me-2"),
            html.Strong("Tiempo estimado de respuesta: "),
            "15-30 minutos para consultas urgentes, 1-2 horas para consultas rutinarias."
        ], color="info", className="mt-3")
    ])
    
    return seguimiento, "tab-estado"

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .card:hover {
                transform: translateY(-2px);
                transition: transform 0.2s ease-in-out;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
            }
            .btn:hover {
                transform: translateY(-1px);
                transition: transform 0.1s ease-in-out;
            }
            .navbar {
                border-bottom: 3px solid #2E8B57;
            }
            .modal-content {
                border-radius: 10px;
            }
            .alert {
                border-radius: 8px;
            }
            .form-control, .form-select {
                border-radius: 6px;
            }
            .card {
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == "__main__":
    app.run_server(debug=True, host="127.0.0.1", port=8050)