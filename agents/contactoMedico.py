import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, Dict
from dotenv import load_dotenv
from agents.agente import Agente

class AgenteContactoMedico(Agente):
    def __init__(self):
        load_dotenv()
        config = {
            "nombre": "Agente Contacto y Resumen Médico",
            "tipo": "contacto_resumen"
        }
        model_config = {
            "model_path": os.getenv("MODEL_PATH"),
            "n_threads": int(os.getenv("LLAMA_N_THREADS", os.cpu_count() or 8)),
            "n_batch": int(os.getenv("LLAMA_N_BATCH", 256)),
            "n_ctx": int(os.getenv("LLAMA_N_CTX", 2048)),
            "temperature": 0.4,
            "max_tokens": 1024,
            "verbose": True
        }
        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "prompts",
            "contacto_medico.txt"
        )
        super().__init__(
            config=config,
            model_config=model_config,
            system_prompt_path=prompt_path
        )
        self.datos_medico = {
            "nombre": "Dr. Juan Pérez",
            "especialidad": "Medicina Familiar",
            "centro": "Centro de Salud Urbano",
            "ubicacion": "Calle Principal #123"
        }

    def iniciar_interaccion(self, session_id: str, mensaje: str) -> Dict:
        """Recopila información del paciente antes de enviar al médico"""
        print(f"[CONTACTO_RESUMEN] Iniciando interacción para sesión {session_id}")
        return {
            "accion": "confirmar_envio",
            "datos_paciente": {
                "nombre": input("Por favor ingrese su nombre completo: "),
                "edad": input("Ingrese su edad: "),
                "telefono": input("Ingrese un teléfono de contacto: ")
            }
        }

    def preguntar(self, session_id: str, pregunta: str, metadata: Optional[Dict] = None) -> Dict:
        if metadata and metadata.get("accion") == "confirmar_envio":
            # Simular generación de resumen médico
            datos = metadata["datos_paciente"]
            resumen = (
                f"Paciente: {datos['nombre']}\n"
                f"Edad: {datos['edad']}\n"
                f"Teléfono: {datos['telefono']}\n"
                f"Motivo: {pregunta}\n"
                "--------------------------------\n"
                "Este documento puede ser compartido con su médico tratante."
            )
            return {
                "output": (
                    f"✉️ Se ha enviado su caso al {self.datos_medico['centro']}\n"
                    f"Médico asignado: {self.datos_medico['nombre']} ({self.datos_medico['especialidad']})\n\n"
                    f"Resumen enviado:\n{resumen}\n\n"
                    "El médico se pondrá en contacto con usted en las próximas 24 horas."
                ),
                "metadata": {
                    "enviado_a": self.datos_medico,
                    "datos_paciente": datos
                }
            }
        # Si no hay metadata, pedir información primero
        return {
            "output": "Para contactar a su médico y generar un resumen, necesitamos algunos datos primero...",
            "metadata": {"necesita_datos": True}
        } 