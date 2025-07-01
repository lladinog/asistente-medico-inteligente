import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, Dict
from dotenv import load_dotenv

from agents.agente import Agente

class AgenteBusquedaCentros(Agente):
    def __init__(self):
        load_dotenv()
        
        config = {
            "nombre": "Agente Búsqueda de Centros",
            "tipo": "geolocalizacion"
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
            "busqueda_centros.txt"
        )

        super().__init__(
            config=config,
            model_config=model_config,
            system_prompt_path=prompt_path
        )
    
    def iniciar_interaccion(self, session_id: str, mensaje: str) -> Optional[Dict]:
        """Inicia la interacción con el agente de búsqueda de centros"""
        print(f"[BUSQUEDA_CENTROS] Iniciando interacción para sesión {session_id}")
        return None
    
    def preguntar(self, session_id: str, pregunta: str, metadata: Optional[Dict] = None) -> Dict:
        # Respuesta temporal hasta implementar geolocalización
        return {
            "output": "🏥 Función de búsqueda de centros en desarrollo. Por ahora, estos son centros de ejemplo:\n"
                      "1. Centro de Salud Urbano (A 1.2 km)\n"
                      "2. Hospital General (A 3.5 km)\n"
                      "3. Clínica Rural (A 5 km)",
            "metadata": {"tipo": "placeholder"}
        }