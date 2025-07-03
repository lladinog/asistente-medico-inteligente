"""
Aplicación principal completamente modular
Utiliza componentes, estilos y callbacks separados
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from agents.orquestador import Orquestador, FuncionalidadMedica
from agents.diagnostico import AgenteDiagnostico
from agents.explicacion import AgenteExplicacionMedica

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
    
    # Configuración inicial
    config = {
        "nombre_app": "Health IA",
        "estilo": dbc.themes.DARKLY
    }

    model_config = {
        "model_path": "modelos/llama-medical.bin",
        "n_ctx": 2048,
        "n_threads": 8
    }

    # Inicializar orquestador
    orquestador = Orquestador(config, model_config)

    # Registrar agentes
    orquestador.registrar_agente(
        FuncionalidadMedica.DIAGNOSTICO,
        AgenteDiagnostico()
    )
    orquestador.registrar_agente(
        FuncionalidadMedica.EXPLICACION_MEDICA,
        AgenteExplicacionMedica()
    )

    # Crear aplicación Dash
    app = dash.Dash(__name__, external_stylesheets=[config["estilo"]])
    app.title = config["nombre_app"]

    # Layout principal con componentes
    app.layout = html.Div(style=MAIN_STYLES['main-container'], children=[
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='session-id', storage_type='session'),
        dcc.Store(id='current-functionality', data='home'),
        dcc.Store(id='sidebar-collapsed', data=False),
        dcc.Store(id='conversations-store', data=[]),
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