from dash import html, dcc
import dash_bootstrap_components as dbc

def create_navbar(current_path=None):
    # Determinar qué link está activo
    def get_item_class(path):
        return "nav-link active" if current_path == path else "nav-link"
    
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Inicio", href="/", className=get_item_class("/"))),
            dbc.NavItem(dbc.NavLink("Diagnóstico", href="/diagnostico", className=get_item_class("/diagnostico"))),
            dbc.NavItem(dbc.NavLink("Análisis de Imágenes", href="/imagenes", className=get_item_class("/imagenes"))),
            dbc.NavItem(dbc.NavLink("Interpretación de Exámenes", href="/examenes", className=get_item_class("/examenes"))),
            dbc.NavItem(dbc.NavLink("Explicación Médica", href="/explicacion", className=get_item_class("/explicacion"))),
            dbc.NavItem(dbc.NavLink("Centros Médicos", href="/centros", className=get_item_class("/centros"))),
            dbc.NavItem(dbc.NavLink("Contacto Médico", href="/contacto", className=get_item_class("/contacto")))
        ],
        brand="Asistente Médico Rural",
        brand_href="/",
        color="primary",
        dark=True,
        className="mb-4"
    )