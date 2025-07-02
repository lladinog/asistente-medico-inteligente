import os
from typing import Optional, Dict
from dotenv import load_dotenv

from agents.agente import Agente
from vision import (
    analizar_tumor_cerebral,
    analizar_quemaduras,
    analizar_radiografia_torax,
    analizar_enfermedad_piel)

class AgenteAnalisisImagenes(Agente):
    def __init__(self):
        load_dotenv()
        
        config = {
            "nombre": "Agente Análisis de Imágenes",
            "tipo": "vision_computadora"
        }

        model_config = {
            "model_path": os.getenv("MODEL_PATH"),
            "n_threads": int(os.getenv("LLAMA_N_THREADS", os.cpu_count() or 8)),
            "n_batch": int(os.getenv("LLAMA_N_BATCH", 256)),
            "n_ctx": int(os.getenv("LLAMA_N_CTX", 2048)),
            "temperature": 0.7,
            "max_tokens": 512,
            "verbose": True
        }

        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "prompts",
            "analisis_imagenes.txt"
        )

        super().__init__(
            config=config,
            model_config=model_config,
            system_prompt_path=prompt_path,
            tools=[analizar_tumor_cerebral,
                   analizar_quemaduras,
                   analizar_radiografia_torax,
                   analizar_enfermedad_piel
                   ]
        )
    
    def iniciar_interaccion(self, session_id: str, mensaje: str) -> Optional[Dict]:
        """Inicia la interacción con el agente de análisis de imágenes"""
        print(f"[ANALISIS_IMAGENES] Iniciando interacción para sesión {session_id}")
        return None
    
    def preguntar(self, session_id: str, pregunta: str, metadata: Optional[Dict] = None) -> Dict:
        self._ensure_llm()
        os.makedirs("historiales", exist_ok=True)

        # Si metadata contiene la ruta de imagen, usar herramientas directamente
        if metadata and "image_path" in metadata:
            resultados = []
            for herramienta in self.tools:
                resultados.append(herramienta.run(metadata["image_path"]))
            return {
                "output": "\n\n".join(resultados),
                "metadata": {"tipo": "inferencia_imagen"}
            }

        # Caso estándar de conversación LLM
        respuesta = self.agente.invoke(
            {"input": pregunta},
            config={"configurable": {"session_id": session_id}}
        )
        return respuesta
