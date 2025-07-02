import os
from typing import Optional, Dict
from dotenv import load_dotenv

from agents.agente import Agente

class AgenteDiagnostico(Agente):
    def __init__(self):
        load_dotenv()
        
        config = {
            "nombre": "Agente Diagnóstico",
            "tipo": "triage_rural"
        }

        model_config = {
            "model_path": os.getenv("MODEL_PATH"),
            "n_threads": int(os.getenv("LLAMA_N_THREADS", os.cpu_count() or 8)),
            "n_batch": int(os.getenv("LLAMA_N_BATCH", 256)),
            "n_ctx": int(os.getenv("LLAMA_N_CTX", 2048)),
            "temperature": 0.3,
            "max_tokens": 512,
            "verbose": True
        }

        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "prompts",
            "diagnostico.txt"
        )

        super().__init__(
            config=config,
            model_config=model_config,
            system_prompt_path=prompt_path
        )
    
    def iniciar_interaccion(self, session_id: str, mensaje: str) -> Optional[Dict]:
        """Inicia la interacción con el agente de diagnóstico"""
        print(f"[DIAGNOSTICO] Iniciando interacción para sesión {session_id}")
        return None
    
    def preguntar(self, session_id: str, pregunta: str, metadata: Optional[Dict] = None) -> Dict:
        respuesta = super().preguntar(session_id, pregunta)
        # Si la respuesta es un string, conviértela en dict
        if isinstance(respuesta, str):
            respuesta = {"output": respuesta}
        # Añadir advertencia médica estándar
        respuesta["output"] += (
            "\n\n⚠️ Importante: Este es un diagnóstico preliminar basado en la información proporcionada. "
            "No sustituye una consulta médica profesional. Si los síntomas persisten o empeoran, "
            "busque atención médica inmediata."
        )
        return respuesta