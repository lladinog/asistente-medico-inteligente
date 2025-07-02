import os
from typing import Optional, Dict
from dotenv import load_dotenv

from agents.agente import Agente

class AgenteExplicacionMedica(Agente):
    def __init__(self):
        load_dotenv()
        config = {
            "nombre": "Agente Explicación Médica",
            "tipo": "explicacion"
        }
        model_config = {
            "model_path": os.getenv("MODEL_PATH"),
            "n_threads": int(os.getenv("LLAMA_N_THREADS", os.cpu_count() or 8)),
            "n_batch": int(os.getenv("LLAMA_N_BATCH", 256)),
            "n_ctx": int(os.getenv("LLAMA_N_CTX", 2048)),
            "temperature": 0.5,
            "max_tokens": 256,
            "verbose": True
        }
        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "prompts",
            "explicacion_medica.txt"
        )
        super().__init__(
            config=config,
            model_config=model_config,
            system_prompt_path=prompt_path
        )
    
    def preguntar(self, session_id: str, pregunta: str, metadata: Optional[Dict] = None) -> Dict:
        respuesta = super().preguntar(session_id, pregunta)
        # Si la respuesta es un string, conviértela en dict
        if isinstance(respuesta, str):
            respuesta = {"output": respuesta}
        # Añadir ejemplo si la explicación es muy técnica
        if "ejemplo" not in respuesta["output"].lower():
            respuesta["output"] += "\n\nEjemplo: " + self._generar_ejemplo(pregunta)
        return respuesta
    
    def _generar_ejemplo(self, termino: str) -> str:
        """Genera un ejemplo simple para el término médico."""
        ejemplos = {
            "hiperglucemia": "Como cuando una persona con diabetes come muchos dulces y su azúcar en sangre sube mucho.",
            "taquicardia": "Como cuando corres rápido y sientes que tu corazón late muy deprisa.",
            "hipertensión": "Como cuando la presión en tus venas es muy alta, incluso en reposo."
        }
        return ejemplos.get(termino.lower(), "Situación común donde esto podría ocurrir...")