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

def create_diagnostico_content():
    """Contenido para la funcionalidad de diagnóstico"""
    return html.Div([
        html.H4("🔍 Diagnóstico Médico", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Análisis detallado de síntomas y posibles diagnósticos.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📋 Síntomas Analizados", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='sintomas-analizados', children=[
                    html.P("Ingresa tus síntomas en el chat para obtener un análisis detallado.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("🏥 Posibles Diagnósticos", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='diagnosticos-posibles', children=[
                    html.P("Los diagnósticos aparecerán aquí después del análisis.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
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

def create_explicacion_content():
    """Contenido para la funcionalidad de explicación médica"""
    return html.Div([
        html.H4("📚 Explicación Médica", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Explicaciones detalladas de términos y conceptos médicos.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("🔤 Términos Explicados", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='terminos-explicados', children=[
                    html.P("Pregunta sobre cualquier término médico en el chat.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
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

def create_interpretacion_examenes_content():
    """Contenido para la funcionalidad de interpretación de exámenes"""
    return html.Div([
        html.H4("🔬 Interpretación de Exámenes", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Análisis e interpretación de resultados de exámenes médicos.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📊 Resultados de Exámenes", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='resultados-examenes', children=[
                    html.P("Sube o describe tus resultados de exámenes en el chat.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📈 Valores de Referencia", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='valores-referencia', children=[
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

def create_resumen_medico_content():
    """Contenido para la funcionalidad de resumen médico"""
    return html.Div([
        html.H4("📋 Resumen Médico", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Generación de resúmenes médicos y reportes.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📝 Información del Paciente", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='info-paciente', children=[
                    html.P("Proporciona información sobre tu caso en el chat.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📄 Resumen Generado", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='resumen-generado', children=[
                    html.P("El resumen médico aparecerá aquí.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card'])
    ])

def create_contacto_medico_content():
    """Contenido para la funcionalidad de contacto médico"""
    return html.Div([
        html.H4("👨‍⚕️ Contacto Médico", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Información de contacto y localización de profesionales de la salud.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("🏥 Centros Médicos Cercanos", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='centros-medicos', children=[
                    html.P("Busca centros médicos en tu área en el chat.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("👨‍⚕️ Especialistas", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='especialistas', children=[
                    html.P("Aquí aparecerán especialistas recomendados.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
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

def create_busqueda_content():
    """Contenido para la funcionalidad de búsqueda"""
    return html.Div([
        html.H4("🔍 Búsqueda Médica", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Búsqueda de información médica y recursos de salud.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📚 Recursos Médicos", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='recursos-medicos', children=[
                    html.P("Busca información médica específica en el chat.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📖 Artículos y Estudios", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='articulos-estudios', children=[
                    html.P("Aquí aparecerán artículos y estudios relevantes.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card'])
    ])

def create_analizar_imagenes_content():
    """Contenido para la funcionalidad de análisis de imágenes"""
    return html.Div([
        html.H4("🖼️ Análisis de Imágenes", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
        html.P("Análisis de imágenes médicas y diagnósticos visuales.", style=FUNCTIONAL_VIEW_STYLES['content-text']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("📸 Imagen Analizada", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='imagen-analizada', children=[
                    html.P("Sube una imagen médica en el chat para su análisis.", 
                           style=FUNCTIONAL_VIEW_STYLES['content-text'])
                ])
            ])
        ], style=FUNCTIONAL_VIEW_STYLES['content-card']),
        
        dbc.Card([
            dbc.CardBody([
                html.H6("🔍 Resultados del Análisis", style=FUNCTIONAL_VIEW_STYLES['content-card-header']),
                html.Div(id='resultados-imagen', children=[
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