from typing import Dict, Optional

class ResumenMedico:
    def preguntar(self, session_id: str, pregunta: str, metadata: Optional[Dict] = None) -> Dict:
        # Generar resumen basado en el historial
        respuesta = super().preguntar(session_id, f"Genera un resumen médico con: {pregunta}")
        # Si la respuesta es un string, conviértela en dict
        if isinstance(respuesta, str):
            respuesta = {"output": respuesta}
        # Formatear como documento médico
        respuesta["output"] = self._formatear_resumen(respuesta["output"])
        return respuesta 