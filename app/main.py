#!/usr/bin/env python3
"""
Punto de entrada principal para la aplicación Asistente Médico Inteligente
"""

import sys
import os

# Agregar el directorio raíz al path para que Python pueda encontrar los módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.insert(0, root_dir)

import dash
import dash_bootstrap_components as dbc
from app.layout.dashboard import create_main_layout
from app.callbacks.dashboard_callbacks import register_callbacks

# Inicializar la app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Asistente Médico Rural"

# Asignar el layout principal
app.layout = create_main_layout()

# Registrar los callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)

