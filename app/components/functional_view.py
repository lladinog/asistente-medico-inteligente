import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import datetime

# Estilos (simulados para el ejemplo)
FUNCTIONAL_VIEW_STYLES = {
    'functional-view': {},
    'functional-close-button': {},
    'functional-content': {},
    'content-card-header': {},
    'content-text': {},
    'content-card': {}
}

# Datos por defecto
DEFAULT_SYMPTOMS = "Fiebre, dolor de cabeza y malestar general"
DEFAULT_DIAGNOSES = [
    {"nombre": "Gripe común", "probabilidad": 65, "urgencia": "Baja"},
    {"nombre": "Infección viral", "probabilidad": 25, "urgencia": "Baja"},
    {"nombre": "Otra condición", "probabilidad": 10, "urgencia": "Media"}
]

DEFAULT_IMAGE_URL = "assets/placeholder-image.jpg"
DEFAULT_IMAGE_ANALYSIS = {
    "hallazgos": [
        {"nombre": "Opacidad pulmonar", "confianza": 78},
        {"nombre": "Sin fracturas visibles", "confianza": 92}
    ],
    "calidad": "Aceptable",
    "confianza_global": 85,
    "anomalias": 2,
    "descripcion": "Se observan pequeñas opacidades en el lóbulo inferior derecho que podrían indicar infección. No se detectan fracturas ni otras anomalías óseas."
}

DEFAULT_EXAM_DATA = {
    "file_url": "assets/placeholder-exam.pdf",
    "results": {
        "Glucosa": {"valor": 110, "min": 70, "max": 100, "unidad": "mg/dL"},
        "Hemoglobina": {"valor": 14.5, "min": 12, "max": 16, "unidad": "g/dL"},
        "Colesterol": {"valor": 190, "min": 0, "max": 200, "unidad": "mg/dL"}
    }
}

def create_functional_view_component():
    """Crea el componente FunctionalView"""
    return html.Div([
        dbc.Button(
            html.I(className="fas fa-times"),
            id='functional-close-button',
            style=FUNCTIONAL_VIEW_STYLES['functional-close-button']
        ),
        html.Div(id='functional-content', style=FUNCTIONAL_VIEW_STYLES['functional-content'])
    ], id='functional-view', style=FUNCTIONAL_VIEW_STYLES['functional-view'])

def create_diagnostico_content(sintomas=None, diagnosticos=None):
    """Contenido para diagnóstico médico con parámetros opcionales"""
    sintomas = sintomas or DEFAULT_SYMPTOMS
    diagnosticos = diagnosticos or DEFAULT_DIAGNOSES
    
    # Datos para el mapa (por defecto Bogotá)
    centros_medicos = pd.DataFrame({
        'lat': [4.60971, 4.65346, 4.62434],
        'lon': [-74.08175, -74.08365, -74.06613],
        'name': ['Hospital Central', 'Clínica Salud', 'Centro Médico ABC'],
        'tipo': ['Hospital', 'Clínica', 'Centro Médico']
    })
    
    fig = px.scatter_mapbox(centros_medicos, lat="lat", lon="lon", 
                          hover_name="name", hover_data=["tipo"],
                          color="tipo",
                          zoom=12, height=300)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return html.Div([
        html.Div([
            html.H4("🔍 Diagnóstico Médico", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
            dbc.Badge("Preliminar", color="warning", className="me-1"),
        ], style={'display': 'flex', 'align-items': 'center', 'gap': '10px'}),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📋 Síntomas Analizados", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        dcc.Markdown(sintomas, style={'whiteSpace': 'pre-line'})
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
                
                dbc.Card([
                    dbc.CardHeader("🏥 Posibles Diagnósticos", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        create_diagnosis_probability_chart(diagnosticos)
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📍 Centros Médicos Cercanos", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        dcc.Graph(figure=fig, config={'displayModeBar': False}),
                        html.Small("Ubicación aproximada del paciente", className="text-muted")
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
                
                dbc.Card([
                    dbc.CardHeader("⚠️ Recomendaciones", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        html.Ul([
                            html.Li("Consulta siempre con un profesional de la salud"),
                            html.Li("Este es solo un análisis preliminar"),
                            html.Li("No reemplaza la evaluación médica profesional")
                        ])
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
            ], width=6)
        ])
    ])

def create_explicacion_content(terminos=None, conceptos=None):
    """Contenido para explicación médica con parámetros opcionales"""
    terminos = terminos or ["Hiperglucemia", "Taquicardia"]
    conceptos = conceptos or {
        "Hiperglucemia": "Niveles de azúcar en sangre más altos de lo normal",
        "Taquicardia": "Frecuencia cardíaca más rápida de lo normal"
    }
    
    return html.Div([
        html.H4("📚 Explicación Médica", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Explicaciones detalladas de términos y conceptos médicos.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🔤 Términos Explicados", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        html.Ul([html.Li(f"{term}: {conceptos[term]}") for term in terminos])
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📖 Conceptos Médicos", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.H6(term, className="mb-2"),
                                html.P(desc, className="mb-3")
                            ]) for term, desc in conceptos.items()
                        ])
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
            ], width=6)
        ])
    ])

def create_interpretacion_examenes_content(file_url=None, results=None):
    """Contenido para interpretación de exámenes con parámetros opcionales"""
    file_url = file_url or DEFAULT_EXAM_DATA["file_url"]
    results = results or DEFAULT_EXAM_DATA["results"]
    
    exam_data = pd.DataFrame({
        'Parametro': list(results.keys()),
        'Valor': [v['valor'] for v in results.values()],
        'Min': [v['min'] for v in results.values()],
        'Max': [v['max'] for v in results.values()],
        'Unidad': [v['unidad'] for v in results.values()]
    })
    
    fig = px.bar(exam_data, x='Parametro', y='Valor', 
                title="Resultados del Examen",
                labels={'Valor': 'Valor (unidad)'},
                hover_data=['Unidad'],
                text='Valor')
    fig.update_traces(marker_color=['#FFA07A' if v > m else '#90EE90' 
                                  for v, m in zip(exam_data['Valor'], exam_data['Max'])])
    
    return html.Div([
        html.H4("🔬 Interpretación de Exámenes", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Análisis e interpretación de resultados de exámenes médicos.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📊 Resultados de Exámenes", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        html.Iframe(src=file_url, style={'width': '100%', 'height': '400px', 'border': '1px solid #ddd'})
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📈 Valores de Referencia", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        dcc.Graph(figure=fig),
                        html.Small("Comparación con rangos normales", className="text-muted")
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
            ], width=6)
        ]),
        
        dbc.Card([
            dbc.CardHeader("⚠️ Importante", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
            dbc.CardBody([
                html.Ul([
                    html.Li("La interpretación es solo informativa"),
                    html.Li("Consulta siempre con tu médico"),
                    html.Li("Los valores pueden variar según el laboratorio")
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card'])
    ])

def create_contacto_medico_content(centros=None, especialistas=None, info_contacto=None):
    """Contenido para contacto médico con parámetros opcionales"""
    centros = centros or [
        {"nombre": "Hospital Central", "direccion": "Calle 123 #45-67", "telefono": "601 1234567", "distancia": "2.5 km"},
        {"nombre": "Clínica Salud", "direccion": "Av. Principal #98-76", "telefono": "601 7654321", "distancia": "3.1 km"}
    ]
    
    especialistas = especialistas or [
        {"nombre": "Dr. Carlos Martínez", "especialidad": "Medicina General", "ubicacion": "Clínica Salud", "disponibilidad": "L-V 8am-5pm"},
        {"nombre": "Dra. Ana Rodríguez", "especialidad": "Pediatría", "ubicacion": "Hospital Central", "disponibilidad": "L-J 10am-6pm"}
    ]
    
    info_contacto = info_contacto or {
        "emergencias": "123",
        "salud_total": "018000123456",
        "atencion_ciudadana": "601 9876543"
    }
    
    # Mapa con centros médicos
    centros_df = pd.DataFrame({
        'lat': [4.60971, 4.65346],
        'lon': [-74.08175, -74.08365],
        'name': [c["nombre"] for c in centros],
        'tipo': ['Hospital', 'Clínica']
    })
    
    fig = px.scatter_mapbox(centros_df, lat="lat", lon="lon", 
                          hover_name="name", hover_data=["tipo"],
                          zoom=12, height=300)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return html.Div([
        html.H4("👨‍⚕️ Contacto Médico", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Información de contacto y localización de profesionales de la salud.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🏥 Centros Médicos Cercanos", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        dcc.Graph(figure=fig, config={'displayModeBar': False}),
                        html.Div([
                            html.Div([
                                html.H6(c["nombre"], className="mt-3"),
                                html.P(c["direccion"], className="mb-1"),
                                html.P(f"Tel: {c['telefono']} - Distancia: {c['distancia']}", className="mb-1 text-muted")
                            ]) for c in centros
                        ])
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("👨‍⚕️ Especialistas", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.H6(e["nombre"], className="mb-1"),
                                html.P(e["especialidad"], className="mb-1"),
                                html.Small(f"{e['ubicacion']} - {e['disponibilidad']}", className="text-muted")
                            ], className="mb-3 p-2 border-bottom") for e in especialistas
                        ])
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
                
                dbc.Card([
                    dbc.CardHeader("📞 Información de Contacto", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        html.Ul([
                            html.Li(f"Emergencias: {info_contacto['emergencias']}"),
                            html.Li(f"Línea salud total: {info_contacto['salud_total']}"),
                            html.Li(f"Atención al ciudadano: {info_contacto['atencion_ciudadana']}")
                        ])
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
            ], width=6)
        ])
    ])

def create_busqueda_content(recursos=None, articulos=None):
    """Contenido para búsqueda médica con parámetros opcionales"""
    recursos = recursos or [
        {"titulo": "Guía de síntomas comunes", "tipo": "PDF", "enlace": "#"},
        {"titulo": "Directorio de especialidades médicas", "tipo": "Web", "enlace": "#"}
    ]
    
    articulos = articulos or [
        {"titulo": "Avances en el tratamiento de la diabetes", "autor": "Dr. López", "año": 2023},
        {"titulo": "Nuevas técnicas de diagnóstico por imagen", "autor": "Dra. Gómez", "año": 2022}
    ]
    
    return html.Div([
        html.H4("🔍 Búsqueda Médica", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Búsqueda de información médica y recursos de salud.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📚 Recursos Médicos", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        html.Ul([
                            html.Li([
                                html.A(r["titulo"], href=r["enlace"], target="_blank"),
                                html.Small(f" ({r['tipo']})", className="text-muted")
                            ]) for r in recursos
                        ])
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📖 Artículos y Estudios", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.H6(a["titulo"], className="mb-1"),
                                html.P(f"{a['autor']} - {a['año']}", className="mb-1 text-muted")
                            ], className="mb-3 p-2 border-bottom") for a in articulos
                        ])
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
            ], width=6)
        ])
    ])

def create_analizar_imagenes_content(image_url=None, analysis_results=None):
    """Contenido para análisis de imágenes con parámetros opcionales"""
    image_url = image_url or DEFAULT_IMAGE_URL
    analysis_results = analysis_results or DEFAULT_IMAGE_ANALYSIS
    
    return html.Div([
        html.H4("🖼️ Análisis de Imágenes", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Análisis de imágenes médicas y diagnósticos visuales.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📸 Imagen Analizada", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        html.Img(src=image_url, style={'width': '100%', 'border-radius': '5px'})
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🔍 Resultados del Análisis", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    dbc.CardBody([
                        html.Div([
                            html.H6("Hallazgos:", className="mb-2"),
                            html.Ul([html.Li(f"{f['nombre']} (confianza: {f['confianza']}%)") 
                                    for f in analysis_results['hallazgos']]),
                            html.Hr(),
                            html.P(analysis_results['descripcion'])
                        ])
                    ])
                ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
            ], width=6)
        ]),
        
        dbc.Card([
            dbc.CardHeader("⚠️ Limitaciones", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
            dbc.CardBody([
                html.Ul([
                    html.Li("El análisis es preliminar"),
                    html.Li("Consulta siempre con un radiólogo"),
                    html.Li("No reemplaza la evaluación profesional")
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card'])
    ])

def create_diagnosis_probability_chart(diagnosticos):
    """Crea gráfico de probabilidad de diagnósticos"""
    data = pd.DataFrame({
        'Diagnóstico': [d['nombre'] for d in diagnosticos],
        'Probabilidad': [d['probabilidad'] for d in diagnosticos],
        'Urgencia': [d['urgencia'] for d in diagnosticos]
    })
    
    fig = px.bar(data, x='Probabilidad', y='Diagnóstico', 
                color='Urgencia', orientation='h',
                labels={'Probabilidad': 'Probabilidad (%)'},
                color_discrete_map={
                    'Alta': '#FF5252',
                    'Media': '#FFA726',
                    'Baja': '#66BB6A'
                })
    fig.update_layout(showlegend=False)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})