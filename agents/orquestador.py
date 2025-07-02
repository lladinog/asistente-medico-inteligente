import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import re
from typing import Dict, Optional
from agents.utils.funcionalidades import FuncionalidadMedica
from agents.agente import Agente

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
        
        # Patrones para clasificación por palabras clave
        self.patrones_clasificacion = {
            FuncionalidadMedica.ANALISIS_IMAGENES.value: [
                r'\b(radiografía|radiografia|rx|rayos?\s*x|tomografía|tomografia|tac|resonancia|rmn|ultrasonido|ecografía|ecografia|imagen|placa)\b',
                r'\b(scanner|escáner|escaneo)\b',
                r'\b(imagen\s*médica|imágenes\s*médicas)\b'
            ],
            FuncionalidadMedica.INTERPRETACION_EXAMENES.value: [
                r'\b(examen|análisis|analisis|laboratorio|resultado|prueba)\b',
                r'\b(sangre|orina|heces|biopsia|cultivo)\b',
                r'\b(hemograma|glicemia|colesterol|triglicéridos|creatinina|urea)\b',
                r'\b(examenes?\s*de\s*laboratorio)\b',
                r'\b(valores?\s*de\s*referencia)\b'
            ],
            FuncionalidadMedica.BUSCADOR_CENTROS.value: [
                r'\b(centro\s*médico|hospital|clínica|clinica|consultorio)\b',
                r'\b(ubicación|ubicacion|dirección|direccion|dónde|donde)\b',
                r'\b(cerca|cercano|próximo|proximo)\b',
                r'\b(buscar|encontrar|localizar)\b.*\b(médico|doctor|hospital|clínica)\b'
            ],
            FuncionalidadMedica.CONTACTO_MEDICO.value: [
                r'\b(contactar|llamar|comunicar|hablar)\b.*\b(médico|doctor)\b',
                r'\b(cita|consulta|appointment)\b',
                r'\b(teléfono|telefono|número|numero)\b.*\b(médico|doctor)\b',
                r'\b(emergencia|urgente|urgencia)\b'
            ],
            FuncionalidadMedica.EXPLICACION.value: [
                r'\b(qué\s*es|que\s*es|explicar|explicación|explicacion)\b',
                r'\b(significa|significado|definición|definicion)\b',
                r'\b(cómo\s*funciona|como\s*funciona|mecanismo)\b',
                r'\b(información|informacion|detalles)\b.*\b(enfermedad|condición|condicion|patología|patologia)\b'
            ]
        }
    
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
            "nombre": "Agente clasificador",
            "tipo": "clasificador"
        }

        clasificador_config = {
            "model_path": os.getenv("MODEL_PATH"),
            "n_threads": int(os.getenv("LLAMA_N_THREADS", os.cpu_count() or 8)),
            "n_ctx": 512,  # Reducido para clasificación rápida
            "temperature": 0.0,  # Determinístico para clasificación
            "max_tokens": 5  # Solo necesitamos una palabra
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
    
    def _clasificar_por_patrones(self, mensaje: str) -> Optional[str]:
        """
        Clasifica el mensaje usando patrones de expresiones regulares.
        
        Args:
            mensaje: Mensaje del usuario
            
        Returns:
            str: Funcionalidad detectada o None si no se encuentra
        """
        mensaje_lower = mensaje.lower()
        
        # Verificar patrones en orden de especificidad
        for funcionalidad, patrones in self.patrones_clasificacion.items():
            for patron in patrones:
                if re.search(patron, mensaje_lower, re.IGNORECASE):
                    print(f"[CLASIFICADOR] Patrón encontrado: {patron} -> {funcionalidad}")
                    return funcionalidad
        
        return None
    
    def _determinar_funcionalidad(self, mensaje: str) -> str:
        """
        Determina la funcionalidad solicitada por el usuario usando un enfoque híbrido.
        
        Args:
            mensaje: Mensaje del usuario a analizar
            
        Returns:
            str: Identificador de la funcionalidad detectada
        """
        # Paso 1: Intentar clasificación por patrones (más rápido y confiable)
        funcionalidad_patron = self._clasificar_por_patrones(mensaje)
        if funcionalidad_patron:
            return funcionalidad_patron
        
        # Paso 2: Si no se encuentra patrón, usar el LLM clasificador
        try:
            # Preparar prompt más específico para el clasificador
            prompt_clasificacion = f"""
            Mensaje del usuario: "{mensaje}"
            
            Clasifica ÚNICAMENTE con una de estas palabras exactas:
            - diagnostico
            - analisis_imagenes  
            - interpretacion_examenes
            - explicacion
            - buscador_centros
            - contacto_medico
            
            Respuesta:"""
            
            respuesta = self.agente_clasificador.preguntar(
                session_id="clasificador_temp",
                pregunta=prompt_clasificacion
            )
            
            # Limpiar y validar respuesta
            funcionalidad = str(respuesta).strip().lower()
            
            # Remover texto extra y quedarse solo con la palabra clave
            palabras_validas = [
                "diagnostico", "analisis_imagenes", "interpretacion_examenes",
                "explicacion", "buscador_centros", "contacto_medico"
            ]
            
            for palabra in palabras_validas:
                if palabra in funcionalidad:
                    print(f"[CLASIFICADOR LLM] Clasificado como: {palabra}")
                    return palabra
            
            print(f"[CLASIFICADOR] Respuesta no válida del LLM: '{funcionalidad}'. Usando diagnóstico por defecto.")
            
        except Exception as e:
            print(f"[ERROR CLASIFICADOR] Error en clasificación LLM: {str(e)}")
        
        # Paso 3: Si todo falla, usar diagnóstico por defecto
        print("[CLASIFICADOR] Usando diagnóstico por defecto")
        return FuncionalidadMedica.DIAGNOSTICO.value
    
    def _es_archivo_pdf(self, mensaje_o_ruta: str) -> bool:
        """
        Verifica si el mensaje contiene una ruta de archivo PDF.
        
        Args:
            mensaje_o_ruta: Mensaje o ruta a verificar
            
        Returns:
            bool: True si es un archivo PDF
        """
        # Verificar si es una ruta de archivo PDF
        if mensaje_o_ruta.lower().endswith('.pdf'):
            return True
        
        # Verificar si el mensaje contiene referencia a un PDF
        if re.search(r'\.pdf\b', mensaje_o_ruta.lower()):
            return True
            
        return False
    
    def procesar_mensaje(self, session_id: Optional[str], mensaje_usuario: str, archivo_path: Optional[str] = None) -> Dict:
        """
        Procesa un mensaje del usuario con detección automática de archivos PDF.
        
        Args:
            session_id: ID de sesión
            mensaje_usuario: Mensaje del usuario
            archivo_path: Ruta del archivo si se envió uno
            
        Returns:
            Dict: Resultado del procesamiento
        """
        if not session_id:
            session_id = self._generar_session_id()
        
        # Verificar si se envió un archivo PDF
        if archivo_path and self._es_archivo_pdf(archivo_path):
            print(f"[ORQUESTADOR] Archivo PDF detectado: {archivo_path}")
            return self.procesar_archivo_medico(session_id, archivo_path, mensaje_usuario)
        
        # Verificar si el mensaje hace referencia a un PDF
        if self._es_archivo_pdf(mensaje_usuario):
            print("[ORQUESTADOR] Referencia a PDF en el mensaje")
            funcionalidad = FuncionalidadMedica.INTERPRETACION_EXAMENES.value
        else:
            # Clasificación normal
            funcionalidad = self._determinar_funcionalidad(mensaje_usuario)
        
        self._cambiar_interfaz(funcionalidad)
        print(f"[ORQUESTADOR] Funcionalidad detectada: {funcionalidad}")
        
        # Obtener agente correspondiente
        agente = self.agentes.get(funcionalidad, self.agentes.get(FuncionalidadMedica.DIAGNOSTICO.value))
        
        if not agente:
            return {
                "session_id": session_id,
                "funcionalidad": funcionalidad,
                "respuesta": {
                    "output": "❌ Agente no disponible para esta funcionalidad",
                    "metadata": {"tipo": "error_agente"}
                },
                "metadata": {"error": "Agente no registrado"}
            }
        
        # Paso 1: Iniciar interacción (preprocesamiento si es necesario)
        metadata = None
        try:
            if hasattr(agente, 'iniciar_interaccion'):
                metadata = agente.iniciar_interaccion(session_id, mensaje_usuario)
        except Exception as e:
            print(f"[WARNING] Fallo en preprocesamiento: {str(e)}. Continuando sin metadata.")
        
        # Paso 2: Pregunta principal
        try:
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
            
        except Exception as e:
            error_msg = f"Error procesando mensaje: {str(e)}"
            self._notificar_error(error_msg)
            
            return {
                "session_id": session_id,
                "funcionalidad": funcionalidad,
                "respuesta": {
                    "output": f"❌ {error_msg}",
                    "metadata": {"tipo": "error_procesamiento"}
                },
                "metadata": {"error": error_msg}
            }
    
    def _notificar_error(self, mensaje: str):
        """Notifica al frontend sobre errores de procesamiento."""
        print(f"[ERROR] {mensaje}")
    
    def _generar_session_id(self) -> str:
        """
        Genera un nuevo ID de sesión único.
        
        Returns:
            str: Nuevo session_id
        """
        return f"sess_{int(time.time())}_{os.urandom(4).hex()}"
    
    def procesar_archivo_medico(self, session_id: Optional[str], archivo_path: str, 
                                patient_context: str = "", patient_level: str = "intermedio") -> Dict:
        """
        Procesa un archivo médico (PDF) enviado desde el frontend.
        
        Args:
            session_id: ID de sesión
            archivo_path: Ruta al archivo subido
            patient_context: Contexto del paciente
            patient_level: Nivel de explicación (simple/intermedio/detallado)
            
        Returns:
            Dict: Resultado del procesamiento
        """
        if not session_id:
            session_id = self._generar_session_id()
        
        # Validar que es un archivo PDF
        if not archivo_path.lower().endswith('.pdf'):
            return {
                "session_id": session_id,
                "funcionalidad": "error",
                "respuesta": {
                    "output": "❌ Formato de archivo no soportado. Solo se permiten archivos PDF.",
                    "metadata": {"tipo": "formato_no_soportado"}
                },
                "metadata": {"error": "Formato no soportado"}
            }
        
        # Clasificar automáticamente como interpretación de exámenes
        funcionalidad = FuncionalidadMedica.INTERPRETACION_EXAMENES.value
        self._cambiar_interfaz(funcionalidad)
        print(f"[ORQUESTADOR] Procesando PDF como: {funcionalidad}")
        
        agente = self.agentes.get(funcionalidad)
        if not agente:
            return {
                "session_id": session_id,
                "funcionalidad": funcionalidad,
                "respuesta": {
                    "output": "❌ Agente de interpretación de exámenes no disponible",
                    "metadata": {"tipo": "error_agente"}
                },
                "metadata": {"error": "Agente no registrado"}
            }
        
        try:
            # Iniciar interacción si el método existe
            metadata = None
            if hasattr(agente, 'iniciar_interaccion'):
                metadata = agente.iniciar_interaccion(session_id, f"Análisis de archivo: {archivo_path}")
            
            # Procesar el archivo PDF
            if hasattr(agente, 'procesar_archivo_pdf'):
                respuesta = agente.procesar_archivo_pdf(
                    session_id=session_id,
                    pdf_path=archivo_path,
                    patient_context=patient_context,
                    patient_level=patient_level
                )
            else:
                # Fallback si el agente no tiene el método específico
                respuesta = agente.preguntar(
                    session_id=session_id,
                    pregunta=f"Por favor analiza este archivo médico: {archivo_path}. Contexto: {patient_context}",
                    metadata=metadata
                )
            
            return {
                "session_id": session_id,
                "funcionalidad": funcionalidad,
                "respuesta": respuesta,
                "metadata": metadata if metadata else {}
            }
            
        except Exception as e:
            error_msg = f"Error procesando archivo médico: {str(e)}"
            self._notificar_error(error_msg)
            
            return {
                "session_id": session_id,
                "funcionalidad": funcionalidad,
                "respuesta": {
                    "output": f"❌ {error_msg}",
                    "metadata": {"tipo": "error_procesamiento"}
                },
                "metadata": {"error": error_msg}
            }
    
    def continuar_conversacion_examenes(self, session_id: str, pregunta: str) -> Dict:
        """
        Continúa una conversación sobre exámenes médicos previamente analizados.
        
        Args:
            session_id: ID de sesión con análisis previo
            pregunta: Pregunta adicional del usuario
            
        Returns:
            Dict: Respuesta contextualizada
        """
        funcionalidad = FuncionalidadMedica.INTERPRETACION_EXAMENES.value
        agente = self.agentes.get(funcionalidad)
        
        if not agente:
            return {
                "session_id": session_id,
                "funcionalidad": funcionalidad,
                "respuesta": {
                    "output": "❌ Agente de interpretación no disponible",
                    "metadata": {"tipo": "error_agente"}
                },
                "metadata": {"error": "Agente no registrado"}
            }
        
        try:
            respuesta = agente.preguntar(
                session_id=session_id,
                pregunta=pregunta,
                metadata={"tipo": "pregunta_contextual"}
            )
            
            return {
                "session_id": session_id,
                "funcionalidad": funcionalidad,
                "respuesta": respuesta,
                "metadata": {"tipo": "conversacion_contextual"}
            }
            
        except Exception as e:
            error_msg = f"Error en conversación contextual: {str(e)}"
            self._notificar_error(error_msg)
            
            return {
                "session_id": session_id,
                "funcionalidad": funcionalidad,
                "respuesta": {
                    "output": f"❌ {error_msg}",
                    "metadata": {"tipo": "error_conversacion"}
                },
                "metadata": {"error": error_msg}
            }
        
