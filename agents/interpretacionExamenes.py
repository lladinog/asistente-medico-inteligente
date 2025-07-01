import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, Dict
from dotenv import load_dotenv

from agents.agente import Agente

class AgenteInterpretacionExamenes(Agente):
    def __init__(self):
        load_dotenv()
        
        config = {
            "nombre": "Agente Interpretación de Exámenes",
            "tipo": "analisis_laboratorio"
        }

        model_config = {
            "model_path": os.getenv("MODEL_PATH"),
            "n_threads": int(os.getenv("LLAMA_N_THREADS", os.cpu_count() or 8)),
            "n_batch": int(os.getenv("LLAMA_N_BATCH", 256)),
            "n_ctx": int(os.getenv("LLAMA_N_CTX", 2048)),
            "temperature": 0.2,
            "max_tokens": 512,
            "verbose": True
        }

        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "prompts",
            "interpretacion_examenes.txt"
        )

        super().__init__(
            config=config,
            model_config=model_config,
            system_prompt_path=prompt_path
        )
    
    def iniciar_interaccion(self, session_id: str, mensaje: str) -> Optional[Dict]:
        """Inicia la interacción con el agente de interpretación de exámenes"""
        print(f"[INTERPRETACION_EXAMENES] Iniciando interacción para sesión {session_id}")
        return None
    
    def preguntar(self, session_id: str, pregunta: str, metadata: Optional[Dict] = None) -> Dict:
        # Respuesta temporal hasta implementar procesamiento de PDF
        return {
            "output": "📊 Función de interpretación de exámenes en desarrollo. Por ahora, ingrese los valores manualmente.",
            "metadata": {"tipo": "placeholder"}
        }