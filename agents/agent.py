import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.llms import LlamaCpp
from agents.conversation import Conversation

os.environ["LLAMA_LOG_LEVEL"] = "WARN"  # Puede ser: "ERROR", "WARN", "INFO", "DEBUG"

class Agente:
    def __init__(self, config: dict, model_config: dict, system_prompt_path: str):
        self.config = config
        self.model_config = model_config
        
        with open(system_prompt_path, encoding="utf-8") as f:
            self.system_prompt = f.read()

        # === 1. Crear plantilla del prompt ===
        self.prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template=(
                f"{self.system_prompt}\n\n"
                "Historial de conversación:\n{history}\n\n"
                "Usuario: {input}\nAsistente:"
            ),
        )

        # === 2. Inicializar modelo ===
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

        # === 3. Construir cadena con historial ===
        self.chain = self.prompt_template | self.llm

        # === 4. Historial por sesión ===
        self.history_factory = lambda session_id: Conversation(
    file_path=f"historiales/{session_id}.json",
    max_tokens=self.model_config.get("n_ctx", 768),
    buffer_extra=self.model_config.get("max_tokens", 256) + 64  # margen razonable
)


        self.agente = RunnableWithMessageHistory(
            self.chain,
            get_session_history=self.history_factory,
            input_messages_key="input",
            history_messages_key="history",
        )

    def preguntar(self, session_id, pregunta):
        os.makedirs("historiales", exist_ok=True)
        respuesta = self.agente.invoke({"input": pregunta}, config={"configurable": {"session_id": session_id}})
        return respuesta


if __name__ == "__main__":
    # === Cargar variables de entorno y rutas antes de crear la clase ===
    load_dotenv()
    model_config = {
        "model_path": os.getenv("MODEL_PATH"),
        "n_threads": int(os.getenv("LLAMA_N_THREADS", os.cpu_count() or 8)),
        "n_batch": int(os.getenv("LLAMA_N_BATCH", 256)),
        "n_ctx": int(os.getenv("LLAMA_N_CTX", 2048)),
        # Puedes agregar más parámetros si lo deseas
    }
    print(model_config.get("n_threads"))
    config = {
        "nombre": "Agente Médico",
        "tipo": "prototipo"
    }
    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "prompts",
        "sistema_prototipo.txt"
    )

    agenteMedico = Agente(config=config, model_config=model_config, system_prompt_path=prompt_path)
    session_id = "005"
    while True:
        pregunta = input("Paciente: ")
        if pregunta.lower() in ("salir", "exit"):
            break
        respuesta = agenteMedico.preguntar(session_id, pregunta)
        print(f"Asistente: {respuesta}\n")