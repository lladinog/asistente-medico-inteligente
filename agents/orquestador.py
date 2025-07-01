import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from typing import Dict, Optional
from agents.utils.funcionalidades import FuncionalidadMedica
from agents.agente import Agente

from dash.dependencies import Output, Input

class Orquestador:
    def __init__(self, config: Dict, model_config: Dict, frontend_callback=None):
        """
        Inicializa el orquestador con configuración y modelos.
        
        Args:
            config: Configuración general del sistema
            model_config: Configuración de los modelos LLM
        """
        self.config = config
        self.model_config = model_config
        self.agentes = {}
        self.agente_clasificador = self._inicializar_agente_clasificador()
        self.frontend_callback = frontend_callback or self._default_callback
    
    def _default_callback(self, funcionalidad: str):
        """Callback por defecto si no se proporciona uno"""
        print(f"[FRONTEND] Cambiando a funcionalidad: {funcionalidad}")
    
    def _cambiar_interfaz(self, funcionalidad: str):
        """Notifica al frontend para cambiar de página"""
        if self.frontend_callback:
            self.frontend_callback(funcionalidad)
        
    def _inicializar_agente_clasificador(self) -> Agente:
        """
        Inicializa el agente especializado en clasificar intenciones.
        Este agente debe ser rápido y ligero.
        """
        config = {
        "nombre": "Agente orquestador",
        "tipo": "clasificador"
        }

        clasificador_config = {
            "model_path": os.getenv("MODEL_PATH"),
            "n_threads": int(os.getenv("LLAMA_N_THREADS", os.cpu_count() or 8)),
            "n_ctx": 512,
            "temperature": 0.1,
            "max_tokens": 10
        }

        prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "prompts",
        "clasificador.txt"
        )

        return Agente(
            config=config,
            model_config=clasificador_config,
            system_prompt_path=prompt_path
        )
    
    def registrar_agente(self, funcionalidad: FuncionalidadMedica, agente: Agente):
        """
        Registra un agente para una funcionalidad específica.
        
        Args:
            funcionalidad: Enum de la funcionalidad médica
            agente: Instancia del agente a registrar
        """
        self.agentes[funcionalidad.value] = agente
    
    def _determinar_funcionalidad(self, mensaje: str) -> str:
        """
        Determina la funcionalidad solicitada por el usuario.
        
        Args:
            mensaje: Mensaje del usuario a analizar
            
        Returns:
            str: Identificador de la funcionalidad detectada
        """
        # Usamos el agente clasificador para determinar la intención
        respuesta = self.agente_clasificador.preguntar(
            session_id="clasificador",
            pregunta=f"Clasifica este mensaje en una de estas categorías: {', '.join([f.value for f in FuncionalidadMedica])}. Solo responde con el nombre de la categoría. Mensaje: {mensaje}"
        )
        funcionalidad = str(respuesta).strip().lower()
        
        # Validamos que sea una funcionalidad conocida
        if funcionalidad not in self.agentes:
            # Si no reconocemos la funcionalidad, usamos diagnóstico por defecto
            return FuncionalidadMedica.DIAGNOSTICO.value
        
        return funcionalidad
    
    
    def procesar_mensaje(self, session_id: Optional[str], mensaje_usuario: str) -> Dict:
        """
        Procesa un mensaje del usuario con el nuevo flujo flexible.
        """
        if not session_id:
            session_id = self._generar_session_id()
        
        funcionalidad = self._determinar_funcionalidad(mensaje_usuario)
        self._cambiar_interfaz(funcionalidad)
        print(f"[ORQUESTADOR] Funcionalidad detectada: {funcionalidad}")
        agente = self.agentes.get(funcionalidad, self.agentes[FuncionalidadMedica.DIAGNOSTICO.value])
        
        # Paso 1: Iniciar interacción (preprocesamiento si es necesario)
        try:
            metadata = agente.iniciar_interaccion(session_id, mensaje_usuario)
        except Exception as e:
            # Si falla el preprocesamiento, delegar al agente de diagnóstico
            print(f"[ERROR] Fallo en preprocesamiento: {str(e)}. Usando agente de diagnóstico por defecto.")
            funcionalidad = FuncionalidadMedica.DIAGNOSTICO.value
            agente = self.agentes[funcionalidad]
            metadata = None
            
            # Notificar al frontend del cambio
            self._cambiar_interfaz(funcionalidad)
            self._notificar_error(f"Fallo en preprocesamiento: {str(e)}")
        
        # Paso 2: Pregunta principal
        respuesta = agente.preguntar(
            session_id=session_id,
            pregunta=mensaje_usuario,
            metadata=metadata
        )
        
        return {
            "session_id": session_id,
            "funcionalidad": funcionalidad,
            "respuesta": respuesta,
            "metadata": metadata if metadata else {}
        }
    
    def _notificar_error(self, mensaje: str):
        """Notifica al frontend sobre errores de procesamiento."""
        print(f"[ERROR] {mensaje}")
        # Ejemplo: frontend.mostrar_error(mensaje)
    
    def _generar_session_id(self) -> str:
        """
        Genera un nuevo ID de sesión único.
        
        Returns:
            str: Nuevo session_id
        """
        return f"sess_{int(time.time())}_{os.urandom(4).hex()}"