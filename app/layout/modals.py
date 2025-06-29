import dash_bootstrap_components as dbc
from dash import html, dcc
from app.app_config import COLORS

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