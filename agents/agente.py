import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dotenv import load_dotenv

os.environ["LLAMA_LOG_LEVEL"] = "NONE" # Puede ser: "ERROR", "WARN", "INFO", "DEBUG"

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.llms import LlamaCpp
from utils.conversation import Conversation
from transformers import AutoTokenizer

 

class Agente(ABC):
    def __init__(self, config: dict, model_config: dict, system_prompt_path: str, tools=None):
        self.config = config
        self.model_config = model_config
        self.tools = tools or []
        self.llm = None  # No inicializar aquí
        
        with open(system_prompt_path, encoding="utf-8") as f:
            self.system_prompt = f.read()

        self.prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template=(
                f"{self.system_prompt}\n\n"
                "Historial de conversación:\n{history}\n\n"
                "Usuario: {input}\nAsistente:"
            ),
        )

        self.chain = None  # Se inicializa cuando se use

        self.history_factory = lambda session_id: Conversation(
            file_path=f"historiales/{session_id}.json",
            max_context_tokens=self.model_config.get("n_ctx", 768),  # Coincide con el modelo
            token_buffer=self.model_config.get("token_buffer", 256),  # Espacio para respuestas
            max_messages=self.model_config.get("max_messages", 10),  # Límite opcional
            tokenizer=self.model_config.get("tokenizer", lambda x: len(x.split()))
        )

        self.agente = None  # Se inicializa cuando se use

    def _ensure_llm(self):
        if self.llm is None:
            self.llm = LlamaCpp(
                model_path=self.model_config.get("model_path"),
                n_ctx=self.model_config.get("n_ctx", 768),
                n_threads=self.model_config.get("n_threads", 8),
                n_batch=self.model_config.get("n_batch", 256),
                temperature=self.model_config.get("temperature", 0.5),
                max_tokens=self.model_config.get("max_tokens", 256),
                stop=self.model_config.get("stop", ["Usuario:", "Paciente:", "Human:", "AI:", "Asistente:"]),
                verbose=self.model_config.get("verbose", True),
            )
            self.chain = self.prompt_template | self.llm
            from langchain_core.runnables import RunnableWithMessageHistory
            self.agente = RunnableWithMessageHistory(
                self.chain,
                get_session_history=self.history_factory,
                input_messages_key="input",
                history_messages_key="history",
            )

    def iniciar_interaccion(self, session_id: str, mensaje: str) -> Optional[Dict[str, Any]]:
        """
        Método opcional para preparar la interacción antes de preguntar.
        Puede ser sobrescrito por los agentes hijos si necesitan preprocesamiento.
        
        Args:
            session_id: ID de la sesión
            mensaje: Mensaje del usuario
            
        Returns:
            Dict con metadata o None si no hay preprocesamiento necesario
        """
        return None

    def preguntar(self, session_id: str, pregunta: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Método principal para realizar preguntas al agente.
        
        Args:
            session_id: ID de la sesión
            pregunta: Pregunta del usuario
            metadata: Metadata opcional de iniciar_interaccion
            
        Returns:
            Respuesta del agente
        """
        self._ensure_llm()
        os.makedirs("historiales", exist_ok=True)
        respuesta = self.agente.invoke(
            {"input": pregunta},
            config={"configurable": {"session_id": session_id}}
        )
        return respuesta


if __name__ == "__main__":
    # === Cargar variables de entorno y rutas antes de crear la clase ===
    load_dotenv()
    hf_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model_config = {
        "model_path": os.getenv("MODEL_PATH"),
        "n_threads": int(os.getenv("LLAMA_N_THREADS", os.cpu_count() or 8)),
        "n_batch": int(os.getenv("LLAMA_N_BATCH", 256)),
        "n_ctx": int(os.getenv("LLAMA_N_CTX", 2048)),
        "max_messages": 3,
        "token_buffer": 256,
        "tokenizer": lambda x: len(hf_tokenizer.encode(x)),  # Tokenizer compatible
        # Puedes agregar más parámetros si lo deseas
    }
    config = {
        "nombre": "Agente Médico",
        "tipo": "prototipo"
    }
    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "prompts",
        "prototipo.txt"
    )

    # Ejemplo: no se pasan tools por defecto
    agenteMedico = Agente(config=config, model_config=model_config, system_prompt_path=prompt_path)
    session_id = "006"
    while True:
        pregunta = input("Paciente: ")
        if pregunta.lower() in ("salir", "exit"):
            break
        respuesta = agenteMedico.preguntar(session_id, pregunta)
        print(f"Asistente: {respuesta}\n")