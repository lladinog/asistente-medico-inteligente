import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from styles.functional_view import FUNCTIONAL_VIEW_STYLES

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

def create_diagnostico_content(sintomas=None, diagnosticos=None, paciente_info=None):
    """Contenido para la funcionalidad de diagnóstico"""
    
    # Componentes default
    default_sintomas = html.P("Ingresa tus síntomas en el chat para obtener un análisis detallado.", 
                             style=FUNCTIONAL_VIEW_STYLES['content-text'])
    default_diagnosticos = html.P("Los diagnósticos aparecerán aquí después del análisis.", 
                                style=FUNCTIONAL_VIEW_STYLES['content-text'])
    
    # Componentes específicos si hay parámetros
    sintomas_content = []
    if sintomas:
        sintomas_content.append(html.H6("Síntomas reportados:", style={'margin-bottom': '10px'}))
        if isinstance(sintomas, list):
            for s in sintomas:
                sintomas_content.append(html.Li(s, style={'margin-left': '20px'}))
        else:
            sintomas_content.append(html.P(sintomas))
    else:
        sintomas_content.append(default_sintomas)
    
    diagnosticos_content = []
    if diagnosticos:
        diagnosticos_content.append(html.H6("Posibles diagnósticos:", style={'margin-bottom': '10px'}))
        if isinstance(diagnosticos, list):
            for d in diagnosticos:
                diagnosticos_content.append(html.Li(d, style={'margin-left': '20px'}))
        else:
            diagnosticos_content.append(html.P(diagnosticos))
    else:
        diagnosticos_content.append(default_diagnosticos)
    
    # Info del paciente si está disponible
    paciente_section = []
    if paciente_info:
        paciente_section = [
            dbc.Card([
                dbc.CardBody([
                    html.H6("👤 Información del Paciente", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                    html.Div([
                        html.P(f"Nombre: {paciente_info.get('nombre', 'No disponible')}"),
                        html.P(f"Edad: {paciente_info.get('edad', 'No disponible')}"),
                        html.P(f"Género: {paciente_info.get('genero', 'No disponible')}")
                    ])
                ])
            ], style=FUNCTIONAL_VIEW_STYLES['content-card'])
        ]
    
    return html.Div([
        html.H4("🔍 Diagnóstico Médico", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Análisis detallado de síntomas y posibles diagnósticos.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        *paciente_section,
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📋 Síntomas Analizados", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='sintomas-analizados', children=sintomas_content)
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("🏥 Posibles Diagnósticos", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='diagnosticos-posibles', children=diagnosticos_content)
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("⚠️ Recomendaciones", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='recomendaciones-diagnostico', children=[
                    html.P("• Consulta siempre con un profesional de la salud", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text']),
                    html.P("• Este es solo un análisis preliminar", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text']),
                    html.P("• No reemplaza la evaluación médica profesional", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card'])
    ])

def create_explicacion_content(termino=None, explicacion=None):
    """Contenido para la funcionalidad de explicación médica"""
    
    # Componente default
    default_content = html.P("Pregunta sobre cualquier término médico en el chat.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
    
    # Componente específico si hay parámetros
    termino_content = []
    if termino and explicacion:
        termino_content.append(html.H6(f"Término: {termino}", style={'margin-bottom': '10px'}))
        termino_content.append(html.P(explicacion))
    else:
        termino_content.append(default_content)
    
    return html.Div([
        html.H4("📚 Explicación Médica", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Explicaciones detalladas de términos y conceptos médicos.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("🔤 Términos Explicados", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='terminos-explicados', children=termino_content)
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📖 Conceptos Médicos", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='conceptos-medicos', children=[
                    html.P("Aquí aparecerán explicaciones de conceptos médicos.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card'])
    ])

def create_interpretacion_examenes_content(file_path=None, resultados=None):
    """Contenido para la funcionalidad de interpretación de exámenes"""
    
    # Componente default
    default_content = html.Div([
        html.P("Sube o describe tus resultados de exámenes en el chat.", 
               style=FUNCTIONAL_VIEW_STYLES['content-text']),
        dcc.Upload(
            id='upload-examenes',
            children=dbc.Button(
                "📎 Adjuntar archivo (PDF o TXT)",
                color="primary",
                className="me-1"
            ),
            multiple=False
        )
    ])
    
    # Componente específico si hay parámetros
    resultados_content = []
    if file_path:
        # Mostrar el archivo o su contenido
        resultados_content.append(html.H6("Archivo adjunto:", style={'margin-bottom': '10px'}))
        resultados_content.append(html.P(f"Archivo: {file_path}"))
        
        # Botón para ver el archivo (simulado)
        resultados_content.append(dbc.Button(
            "👁️ Ver archivo",
            color="info",
            className="me-1",
            style={'margin-top': '10px'}
        ))
    else:
        resultados_content.append(default_content)
    
    # Resultados del análisis si están disponibles
    analisis_content = []
    if resultados:
        analisis_content.append(html.H6("Interpretación:", style={'margin-bottom': '10px'}))
        if isinstance(resultados, dict):
            for key, value in resultados.items():
                analisis_content.append(html.P(f"{key}: {value}"))
        else:
            analisis_content.append(html.P(resultados))
    
    return html.Div([
        html.H4("🔬 Interpretación de Exámenes", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Análisis e interpretación de resultados de exámenes médicos.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📊 Resultados de Exámenes", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='resultados-examenes', children=resultados_content)
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📈 Análisis de Resultados", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='valores-referencia', children=analisis_content if analisis_content else [
                    html.P("Aquí aparecerán los valores normales y su interpretación.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("⚠️ Importante", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='importante-examenes', children=[
                    html.P("• La interpretación es solo informativa", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text']),
                    html.P("• Consulta siempre con tu médico", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text']),
                    html.P("• Los valores pueden variar según el laboratorio", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card'])
    ])

def create_contacto_medico_content(medico_info=None, centros=None):
    """Contenido para la funcionalidad de contacto médico"""
    
    # Componente default
    default_content = html.P("Busca centros médicos en tu área en el chat.", 
                            style=FUNCTIONAL_VIEW_STYLES['content-text'])
    
    # Componente específico si hay parámetros
    medico_content = []
    if medico_info:
        medico_content.append(html.H6("Médico asignado:", style={'margin-bottom': '10px'}))
        medico_content.append(html.P(f"Nombre: {medico_info.get('nombre', 'No disponible')}"))
        medico_content.append(html.P(f"Especialidad: {medico_info.get('especialidad', 'No disponible')}"))
        medico_content.append(html.P(f"Contacto: {medico_info.get('contacto', 'No disponible')}"))
    else:
        medico_content.append(default_content)
    
    # Lista de centros si está disponible
    centros_content = []
    if centros:
        centros_content.append(html.H6("Centros médicos recomendados:", style={'margin-bottom': '10px'}))
        if isinstance(centros, list):
            for centro in centros:
                centros_content.append(html.Li(
                    html.Div([
                        html.Strong(centro.get('nombre', 'Centro médico')),
                        html.Br(),
                        html.Span(f"Dirección: {centro.get('direccion', 'No disponible')}"),
                        html.Br(),
                        html.Span(f"Teléfono: {centro.get('telefono', 'No disponible')}")
                    ]),
                    style={'margin-bottom': '10px'}
                ))
        else:
            centros_content.append(html.P(centros))
    
    return html.Div([
        html.H4("👨‍⚕️ Contacto Médico", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Información de contacto y localización de profesionales de la salud.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("🏥 Centros Médicos Cercanos", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='centros-medicos', children=centros_content if centros_content else [
                    html.P("Busca centros médicos en tu área en el chat.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("👨‍⚕️ Especialista Asignado", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='especialistas', children=medico_content)
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📞 Información de Contacto", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='info-contacto', children=[
                    html.P("Teléfonos, direcciones y horarios de atención.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card'])
    ])

def create_busqueda_content(termino=None, resultados=None):
    """Contenido para la funcionalidad de búsqueda"""
    
    # Componente default
    default_content = html.P("Busca información médica específica en el chat.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
    
    # Componente específico si hay parámetros
    busqueda_content = []
    if termino:
        busqueda_content.append(html.H6(f"Búsqueda: {termino}", style={'margin-bottom': '10px'}))
    else:
        busqueda_content.append(default_content)
    
    # Resultados de búsqueda si están disponibles
    resultados_content = []
    if resultados:
        resultados_content.append(html.H6("Resultados encontrados:", style={'margin-bottom': '10px'}))
        if isinstance(resultados, list):
            for r in resultados:
                resultados_content.append(html.Div([
                    html.A(r.get('titulo', 'Sin título'), href=r.get('enlace', '#'), target="_blank"),
                    html.P(r.get('descripcion', 'Sin descripción')),
                    html.Hr()
                ]))
        else:
            resultados_content.append(html.P(resultados))
    
    return html.Div([
        html.H4("🔍 Búsqueda Médica", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Búsqueda de información médica y recursos de salud.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📚 Recursos Médicos", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='recursos-medicos', children=busqueda_content)
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📖 Resultados de Búsqueda", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='articulos-estudios', children=resultados_content if resultados_content else [
                    html.P("Aquí aparecerán artículos y estudios relevantes.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card'])
    ])

def create_analizar_imagenes_content(image_path=None, resultados=None):
    """Contenido para la funcionalidad de análisis de imágenes"""
    
    # Componente default
    default_content = html.Div([
        html.P("Sube una imagen médica en el chat para su análisis.", 
               style=FUNCTIONAL_VIEW_STYLES['content-text']),
        dcc.Upload(
            id='upload-imagen',
            children=dbc.Button(
                "📷 Adjuntar imagen",
                color="primary",
                className="me-1"
            ),
            multiple=False
        )
    ])
    
    # Componente específico si hay parámetros
    imagen_content = []
    if image_path:
        imagen_content.append(html.H6("Imagen para análisis:", style={'margin-bottom': '10px'}))
        imagen_content.append(html.Img(src=image_path, style={'max-width': '100%', 'max-height': '300px'}))
        imagen_content.append(dbc.Button(
            "🔄 Cambiar imagen",
            color="secondary",
            className="me-1",
            style={'margin-top': '10px'}
        ))
    else:
        imagen_content.append(default_content)
    
    # Resultados del análisis si están disponibles
    analisis_content = []
    if resultados:
        analisis_content.append(html.H6("Hallazgos:", style={'margin-bottom': '10px'}))
        if isinstance(resultados, dict):
            for key, value in resultados.items():
                analisis_content.append(html.P(f"{key}: {value}"))
        else:
            analisis_content.append(html.P(resultados))
    
    return html.Div([
        html.H4("🖼️ Análisis de Imágenes", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Análisis de imágenes médicas y diagnósticos visuales.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📸 Imagen Analizada", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='imagen-analizada', children=imagen_content)
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("🔍 Resultados del Análisis", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='resultados-imagen', children=analisis_content if analisis_content else [
                    html.P("Los resultados del análisis aparecerán aquí.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("⚠️ Limitaciones", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='limitaciones-imagen', children=[
                    html.P("• El análisis es preliminar", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text']),
                    html.P("• Consulta siempre con un radiólogo", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text']),
                    html.P("• No reemplaza la evaluación profesional", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card'])
    ])

def create_centros_cercanos_content(municipio=None, centros=None):
    """Contenido para la funcionalidad de búsqueda de centros cercanos"""
    
    # Mapa de Colombia por defecto
    mapa_content = html.Iframe(
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d16284026.303741757!2d-83.72287695!3d4.57086835!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x8e15a43aae1594a3%3A0x9a0d9a04eff2a340!2sColombia!5e0!3m2!1ses!2sco!4v1620000000000!5m2!1ses!2sco",
        width="100%",
        height="300",
        style={"border": "0"},
        allowFullScreen="",
        loading="lazy"
    )
    
    # Actualizar mapa si se selecciona un municipio
    if municipio:
        mapa_content = html.Iframe(
            src=f"https://www.google.com/maps/embed/v1/place?key=YOUR_API_KEY&q={municipio},Colombia",
            width="100%",
            height="300",
            style={"border": "0"},
            allowFullScreen="",
            loading="lazy"
        )
    
    # Selector de municipio
    municipio_selector = dcc.Dropdown(
        id='municipio-selector',
        options=[
            {'label': 'Bogotá', 'value': 'Bogotá'},
            {'label': 'Medellín', 'value': 'Medellín'},
            {'label': 'Cali', 'value': 'Cali'},
            {'label': 'Barranquilla', 'value': 'Barranquilla'},
            {'label': 'Cartagena', 'value': 'Cartagena'},
            {'label': 'Otra ciudad', 'value': 'other'}
        ],
        placeholder="Selecciona tu municipio",
        value=municipio if municipio else None
    )
    
    # Lista de centros si está disponible
    centros_content = []
    if centros:
        centros_content.append(html.H6("Centros médicos cercanos:", style={'margin-bottom': '10px'}))
        if isinstance(centros, list):
            for centro in centros:
                centros_content.append(html.Div([
                    html.H5(centro.get('nombre', 'Centro médico')),
                    html.P(f"📍 {centro.get('direccion', 'Dirección no disponible')}"),
                    html.P(f"📞 {centro.get('telefono', 'Teléfono no disponible')}"),
                    html.P(f"⏰ {centro.get('horario', 'Horario no disponible')}"),
                    html.P(f"📌 Distancia: {centro.get('distancia', '?')} km"),
                    html.Hr()
                ]))
        else:
            centros_content.append(html.P(centros))
    
    return html.Div([
        html.H4("🏥 Centros Médicos Cercanos", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Encuentra los centros de atención más cercanos a tu ubicación.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("🗺️ Ubicación", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                municipio_selector,
                html.Div(mapa_content, style={'margin-top': '15px'})
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("🏥 Centros de Salud", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='lista-centros', children=centros_content if centros_content else [
                    html.P("Selecciona un municipio para ver los centros médicos disponibles.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("ℹ️ Información Adicional", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div([
                    html.P("• Los datos se actualizan periódicamente", style=FUNCTIONAL_VIEW_STYLES['content-text']),
                    html.P("• Verifica horarios antes de visitar", style=FUNCTIONAL_VIEW_STYLES['content-text']),
                    html.P("• Algunos centros requieren cita previa", style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card'])
    ])