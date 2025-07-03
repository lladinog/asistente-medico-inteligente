"""
Aplicación principal completamente modular
Utiliza componentes, estilos y callbacks separados para todos los agentes
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["CLICOLOR"] = "0"

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from agents.orquestador import Orquestador, FuncionalidadMedica
from agents.diagnostico import AgenteDiagnostico
from agents.analizarImagenes import AgenteAnalisisImagenes
from agents.interpretacionExamenes import AgenteInterpretacionExamenes
from agents.explicacion import AgenteExplicacionMedica
from agents.busqueda import AgenteBusquedaCentros
from agents.contactoMedico import AgenteContactoMedico

# Importar componentes
from components.sidebar import create_sidebar_component
from components.chat import create_chat_component
from components.functional_view import create_functional_view_component

# Importar estilos
from styles.main import MAIN_STYLES

# Importar callbacks
from callbacks.sidebar import register_sidebar_callbacks
from callbacks.chat import register_chat_callbacks
from callbacks.navigation import register_navigation_callbacks

def create_app():
    """Crea y configura la aplicación Dash"""
    
    # Inicializar orquestador sin frontend_callback
    orquestador = Orquestador()

    # Registrar todos los agentes disponibles
    orquestador.registrar_agente(
        FuncionalidadMedica.DIAGNOSTICO,
        AgenteDiagnostico()
    )
    orquestador.registrar_agente(
        FuncionalidadMedica.ANALISIS_IMAGENES,
        AgenteAnalisisImagenes()
    )
    orquestador.registrar_agente(
        FuncionalidadMedica.INTERPRETACION_EXAMENES,
        AgenteInterpretacionExamenes()
    )
    orquestador.registrar_agente(
        FuncionalidadMedica.EXPLICACION,
        AgenteExplicacionMedica()
    )
    orquestador.registrar_agente(
        FuncionalidadMedica.BUSCADOR_CENTROS,
        AgenteBusquedaCentros()
    )
    orquestador.registrar_agente(
        FuncionalidadMedica.CONTACTO_MEDICO,
        AgenteContactoMedico()
    )

    # Crear aplicación Dash
    external_stylesheets = [
        dbc.themes.DARKLY,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"
    ]
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
    app.title = "Health IA"

    # Layout principal con componentes
    app.layout = html.Div(style=MAIN_STYLES['main-container'], children=[
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='session-id', storage_type='session'),
        dcc.Store(id='current-functionality', data='home'),
        dcc.Store(id='sidebar-collapsed', data=False),
        dcc.Store(id='conversations-store', data=[]),
        dcc.Store(id='sidebar-editing-title', data=None),
        dcc.Upload(id='upload-document', children=None, multiple=True),
        
        # Botón flotante para abrir sidebar (visible cuando está cerrado)
        dbc.Button(
            html.I(className="fas fa-bars"),
            id='floating-sidebar-toggle',
            style=MAIN_STYLES['floating-sidebar-toggle']
        ),
        
        # Sidebar
        create_sidebar_component(),
        
        # Chat principal
        create_chat_component(),
        
        # Vista funcional
        create_functional_view_component()
    ])

    # Registrar todos los callbacks
    register_sidebar_callbacks(app)
    register_chat_callbacks(app, orquestador)
    register_navigation_callbacks(app)

    return app

def main():
    """Función principal para ejecutar la aplicación"""
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    main() 