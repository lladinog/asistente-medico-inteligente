import dash
from dash import Input, Output, State, dcc, html
import dash_bootstrap_components as dbc
from datetime import datetime
from app.app_config import COLORS, CENTROS_MEDICOS, COORDENADAS_CENTROS, MEDICOS_ASIGNADOS
from app.layout.modals import (
    create_diagnostico_content,
    create_imagenes_content,
    create_examenes_content,
    create_explicacion_content,
    create_centros_content,
    create_resumen_content
)

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

def register_callbacks(app):
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
        
        if especialidad != "todas":
            centros = [centro for centro in centros if especialidad in centro["especialidades"]]
            coordenadas = [coord for coord in coordenadas 
                          if any(c["nombre"] == coord["nombre"] for c in centros)]
        
        if not centros:
            return dbc.Alert("No se encontraron centros médicos con los criterios especificados.", color="warning"), ""
        
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
    def generar_resumen(n_clicks, nombre, cedula, edad, telefono, motivo, sintomas, prioridad):
        if not n_clicks:
            return "", "tab-resumen", ""
        
        if not all([nombre, cedula, edad, telefono, motivo, sintomas]):
            return dbc.Alert("Por favor completa todos los campos requeridos.", color="danger"), "tab-resumen", ""
        
        if prioridad == "emergencia":
            medico = {"nombre": "Dr. Emergency Response", "especialidad": "Medicina de Urgencias", 
                     "centro": "Hospital San Rafael", "disponibilidad": "24/7", "tiempo_respuesta": "Inmediato"}
        elif prioridad == "mayor":
            medico = MEDICOS_ASIGNADOS[0]
            medico["tiempo_respuesta"] = "15-30 minutos"
        else:
            medico = MEDICOS_ASIGNADOS[1]
            medico["tiempo_respuesta"] = "1-2 horas"
        
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
        
        advertencia = mostrar_advertencia_etica()
        
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