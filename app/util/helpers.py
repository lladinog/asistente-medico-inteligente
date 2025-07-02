"""
Funciones de utilidad comunes para la aplicación
"""

import datetime
from typing import List, Dict, Any
from agents.orquestador import FuncionalidadMedica

def generate_session_id() -> str:
    """Genera un ID de sesión único"""
    return f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(datetime.datetime.now())}"

def format_timestamp(timestamp: str) -> str:
    """Formatea un timestamp para mostrar"""
    try:
        dt = datetime.datetime.fromisoformat(timestamp)
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return timestamp

def truncate_text(text: str, max_length: int = 50) -> str:
    """Trunca texto a una longitud máxima"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def create_conversation_item(title: str, session_id: str) -> Dict[str, Any]:
    """Crea un elemento de conversación"""
    return {
        'id': session_id,
        'title': truncate_text(title),
        'timestamp': datetime.datetime.now().isoformat()
    }

def merge_styles(*style_dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Combina múltiples diccionarios de estilos"""
    merged = {}
    for style_dict in style_dicts:
        if style_dict:
            merged.update(style_dict)
    return merged

def validate_input(text: str) -> bool:
    """Valida que el texto de entrada no esté vacío"""
    return text and text.strip() and len(text.strip()) > 0

def sanitize_text(text: str) -> str:
    """Sanitiza el texto de entrada"""
    if not text:
        return ""
    return text.strip()

def get_functionality_from_path(pathname: str) -> str:
    """Obtiene la funcionalidad basada en el pathname"""
    if pathname == '/diagnostico':
        return 'diagnostico'
    elif pathname == '/explicacion':
        return 'explicacion_medica'
    else:
        return 'home'

def generar_mensaje_bienvenida():
    menu = "\n".join(
        [
            f"{i+1}. {f.emoji} {f.label} ({f.key})"
            for i, f in enumerate(FuncionalidadMedica)
        ]
    )
    return (
        f"¡Hola! Soy tu asistente médico inteligente. Estas son mis funcionalidades:\n\n"
        f"{menu}\n\n"
        "Puedes escribir el número o el nombre de la funcionalidad que deseas usar."
    ) 