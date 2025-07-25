import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import re
from typing import Dict, Optional
from utils.funcionalidades import FuncionalidadMedica
from agents.agente import Agente

class Orquestador:
    def __init__(self):
        """
        Inicializa el orquestador con configuración y modelos.
        """
        # Configuración inicial
        config = {
            "nombre_app": "Health IA",
            "tipo": "Orquestador",
        }

        model_config = {
            "model_path": os.getenv("MODEL_PATH"),
            "n_ctx": 2048,
            "n_threads": int(os.getenv("LLAMA_N_THREADS", os.cpu_count() or 8))
        }
        
        self.config = config
        self.model_config = model_config
        self.agentes = {}
        self.agente_clasificador = self._inicializar_agente_clasificador()

        self.sesiones_activas = {}  # {session_id: {"funcionalidad": str, "ultimo_agente": Agente, "timestamp": float}}
        self.timeout_sesion = 3600  # 1 hora de timeout por defecto
        
        # Patrones para clasificación por palabras clave
        self.patrones_clasificacion = {
            FuncionalidadMedica.ANALISIS_IMAGENES.key: [
                r'\b(radiografía|radiografia|rx|rayos?\s*x|tomografía|tomografia|tac|resonancia|rmn|ultrasonido|ecografía|ecografia|imagen|placa)\b',
                r'\b(scanner|escáner|escaneo)\b',
                r'\b(imagen\s*médica|imágenes\s*médicas)\b'
            ],
            FuncionalidadMedica.INTERPRETACION_EXAMENES.key: [
                r'\b(examen|análisis|analisis|laboratorio|resultado|prueba)\b',
                r'\b(sangre|orina|heces|biopsia|cultivo)\b',
                r'\b(hemograma|glicemia|colesterol|triglicéridos|creatinina|urea)\b',
                r'\b(examenes?\s*de\s*laboratorio)\b',
                r'\b(valores?\s*de\s*referencia)\b'
            ],
            FuncionalidadMedica.BUSCADOR_CENTROS.key: [
                r'\b(centro\s*médico|hospital|clínica|clinica|consultorio)\b',
                r'\b(ubicación|ubicacion|dirección|direccion|dónde|donde)\b',
                r'\b(cerca|cercano|próximo|proximo)\b',
                r'\b(buscar|encontrar|localizar)\b.*\b(médico|doctor|hospital|clínica)\b'
            ],
             FuncionalidadMedica.CONTACTO_MEDICO.key: [
                r'\b(contactar|llamar|comunicar|hablar)\b.*\b(médico|doctor)\b',
                r'\b(segunda\s*opinión|segunda\s*opinion|opinión\s*médica|opinion\s*medica)\b',
                r'\b(consultar\s*médico|consultar\s*doctor|consulta\s*médica|consulta\s*medica)\b',
                r'\b(enviar\s*caso|enviar\s*a\s*médico|enviar\s*a\s*doctor)\b',
                r'\b(necesito\s*médico|necesito\s*doctor|quiero\s*médico|quiero\s*doctor)\b',
                r'\b(cita|consulta|appointment)\b',
                r'\b(teléfono|telefono|número|numero)\b.*\b(médico|doctor)\b',
                r'\b(emergencia|urgente|urgencia)\b',
                r'\b(derivar|referir|remitir)\b.*\b(médico|doctor|especialista)\b',
                r'\b(evaluación\s*médica|evaluacion\s*medica|revisión\s*médica|revision\s*medica)\b'
            ],
            FuncionalidadMedica.EXPLICACION.key: [
                r'\b(qué\s*es|que\s*es|explicar|explicación|explicacion)\b',
                r'\b(significa|significado|definición|definicion)\b',
                r'\b(cómo\s*funciona|como\s*funciona|mecanismo)\b',
                r'\b(información|informacion|detalles)\b.*\b(enfermedad|condición|condicion|patología|patologia)\b'
            ]
        }
    
    def _limpiar_sesiones_expiradas(self):
        """Limpia sesiones que han expirado"""
        tiempo_actual = time.time()
        sesiones_expiradas = []
        
        for session_id, info in self.sesiones_activas.items():
            if tiempo_actual - info["timestamp"] > self.timeout_sesion:
                sesiones_expiradas.append(session_id)
        
        for session_id in sesiones_expiradas:
            del self.sesiones_activas[session_id]
            print(f"[SESION] Sesión expirada: {session_id}")
    
    def _actualizar_sesion(self, session_id: str, funcionalidad: str, agente: Agente):
        """Actualiza o crea una sesión activa"""
        self.sesiones_activas[session_id] = {
            "funcionalidad": funcionalidad,
            "ultimo_agente": agente,
            "timestamp": time.time()
        }
        print(f"[SESION] Sesión actualizada: {session_id} -> {funcionalidad}")
    
    def _obtener_sesion(self, session_id: str) -> Optional[Dict]:
        """Obtiene información de una sesión activa"""
        self._limpiar_sesiones_expiradas()
        return self.sesiones_activas.get(session_id)
    
    def _es_pregunta_contextual(self, mensaje: str) -> bool:
        """
        Determina si el mensaje es una pregunta contextual que debería 
        continuar con el mismo agente de la sesión anterior.
        """
        # Palabras que indican continuidad en la conversación
        palabras_contextuales = [
            r'\b(y\s*)?qué\s*más\b',
            r'\b(y\s*)?además\b',
            r'\b(y\s*)?también\b',
            r'\bexplica\s*mejor\b',
            r'\bmás\s*detalles?\b',
            r'\by\s*eso\s*qué\s*significa\b',
            r'\bpero\b',
            r'\bentonces\b',
            r'\by\s*si\b',
            r'\by\s*cómo\b',
            r'\by\s*por\s*qué\b',
            r'\by\s*cuándo\b',
            r'\bgracias.*y\b',
            r'\bokay.*y\b',
            r'\bentendido.*y\b'
        ]
        
        mensaje_lower = mensaje.lower().strip()
        
        # Verificar patrones contextuales
        for patron in palabras_contextuales:
            if re.search(patron, mensaje_lower):
                return True
        
        # Verificar si es una pregunta muy corta (probablemente contextual)
        if len(mensaje.split()) <= 3 and any(palabra in mensaje_lower for palabra in ['qué', 'cómo', 'por qué', 'cuándo', 'dónde']):
            return True
        
        return False
    
    def _inicializar_agente_clasificador(self) -> Agente:
        """
        Inicializa el agente especializado en clasificar intenciones.
        Este agente debe ser rápido y ligero.
        """
        config = {
        "nombre": "Agente orquestador",
        "tipo": "Clasificador"
        }

        clasificador_config = {
            "model_path": self.model_config.get("model_path"),
            "n_threads": self.model_config.get("n_threads", 8),
            "model_path": self.model_config.get("model_path"),
            "n_threads": self.model_config.get("n_threads", 8),
            "n_ctx": 1024,
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
        """
        self.agentes[funcionalidad.key] = agente
    
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
    
    def _detectar_funcionalidad_directa(self, mensaje: str) -> Optional[Dict]:
        """
        Si el mensaje es un número válido o el nombre exacto de una funcionalidad,
        retorna la respuesta por defecto completa (dict). Si no, retorna None.
        """
        mensajes_por_defecto = {
            "diagnostico": "Hola, soy el agente de diagnóstico. Puedes contarme tus síntomas o dudas médicas y te orientaré.",
            "analisis_imagenes": "Hola, soy el agente de análisis de imágenes. Sube una imagen médica (radiografía, TAC, etc.) y la analizaré.",
            "interpretacion_examenes": "Hola, soy el agente de interpretación de exámenes. Sube tu archivo de resultados de laboratorio o hazme una pregunta sobre tus exámenes.",
            "explicacion": "Hola, soy el agente de explicaciones médicas. Pregúntame sobre enfermedades, términos médicos o resultados y te lo explico.",
            "buscador_centros": "Hola, soy el agente buscador de centros médicos. Pregúntame por hospitales, clínicas o centros cercanos.",
            "contacto_medico": "Hola, soy el agente de contacto médico. Te ayudo a comunicarte o agendar una cita con un profesional de la salud."
        }
        mensaje_limpio = mensaje.strip().lower()
        funcionalidades = list(FuncionalidadMedica)
        if mensaje_limpio.isdigit():
            idx = int(mensaje_limpio) - 1
            if 0 <= idx < len(funcionalidades):
                funcionalidad_key = funcionalidades[idx].key
                mensaje_defecto = mensajes_por_defecto.get(funcionalidad_key, "Hola, ¿en qué puedo ayudarte?")
                return {
                    "funcionalidad": funcionalidad_key,
                    "respuesta": {
                        "output": mensaje_defecto,
                        "metadata": {"tipo": "mensaje_defecto"}
                    },
                    "metadata": {"info": "respuesta_defecto_funcionalidad"}
                }
        for funcionalidad in funcionalidades:
            if mensaje_limpio == funcionalidad.key:
                mensaje_defecto = mensajes_por_defecto.get(funcionalidad.key, "Hola, ¿en qué puedo ayudarte?")
                return {
                    "funcionalidad": funcionalidad.key,
                    "respuesta": {
                        "output": mensaje_defecto,
                        "metadata": {"tipo": "mensaje_defecto"}
                    },
                    "metadata": {"info": "respuesta_defecto_funcionalidad"}
                }
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
        return FuncionalidadMedica.DIAGNOSTICO.key
    
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
    
    def is_image(self, mensaje: str) -> bool:
        """
        Verifica si el mensaje contiene una referencia a una imagen.
        
        Args:
            mensaje: Mensaje del usuario a verificar
            
        Returns:
            bool: True si es una imagen
        """
        return bool(re.search(r'\.(jpg|jpeg|png|gif|bmp|tiff|webp)$', mensaje.lower()))
    
    def procesar_mensaje(self, session_id: Optional[str], mensaje_usuario: str, archivo_path: Optional[str] = None) -> Dict:
        """
        Procesa un mensaje del usuario con detección automática de archivos PDF.
        """
        if not session_id:
            session_id = self._generar_session_id()

        # Detección directa de funcionalidad y respuesta por defecto
        respuesta_directa = self._detectar_funcionalidad_directa(mensaje_usuario)
        if respuesta_directa:
            respuesta_directa["session_id"] = session_id
            return respuesta_directa
        
        # Verificar si se envió un archivo PDF
        if archivo_path and self._es_archivo_pdf(archivo_path):
            print(f"[ORQUESTADOR] Archivo PDF detectado: {archivo_path}")
            return self.procesar_archivo_medico(session_id, archivo_path, mensaje_usuario)
        
        if archivo_path and self.is_image(archivo_path):
            print(f"[ORQUESTADOR] Imagen médica detectada: {archivo_path}")
            return self.procesar_imagen_medica(session_id, archivo_path, mensaje_usuario)
        
        # Verificar si el mensaje hace referencia a un PDF
        if self._es_archivo_pdf(mensaje_usuario):
            print("[ORQUESTADOR] Referencia a PDF en el mensaje")
            funcionalidad = FuncionalidadMedica.INTERPRETACION_EXAMENES.key
        else:
            # Clasificación normal
            funcionalidad = self._determinar_funcionalidad(mensaje_usuario)
        
        print(f"[ORQUESTADOR] Funcionalidad detectada: {funcionalidad}")
        
        # Obtener agente correspondiente
        agente = self.agentes.get(funcionalidad, self.agentes.get(FuncionalidadMedica.DIAGNOSTICO.key))
        
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
            # Si falla el preprocesamiento, delegar al agente de diagnóstico
            print(f"[ERROR] Fallo en preprocesamiento: {str(e)}. Usando agente de diagnóstico por defecto.")
            funcionalidad = FuncionalidadMedica.DIAGNOSTICO.key
            agente = self.agentes[funcionalidad]
            metadata = None
            
            self._notificar_error(f"Fallo en preprocesamiento: {str(e)}")
        
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
        """Notifica sobre errores de procesamiento."""
        print(f"[ERROR] {mensaje}")
    
    def _generar_session_id(self) -> str:
        """
        Genera un nuevo ID de sesión único.
        """
        return f"sess_{int(time.time())}_{os.urandom(4).hex()}"
    
    def procesar_archivo_medico(self, session_id: Optional[str], archivo_path: str, 
                                patient_context: str = "", patient_level: str = "intermedio") -> Dict:
        """
        Procesa un archivo médico (PDF) enviado desde el frontend.
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
        funcionalidad = FuncionalidadMedica.INTERPRETACION_EXAMENES.key
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
    def procesar_imagen_medica(self, session_id: Optional[str], imagen_path: str, mensaje : str) -> Dict:
        """
        Procesa una imagen médica enviada desde el frontend.
        """
        if not session_id:
            session_id = self._generar_session_id()

        # Validar que es una imagen
        if not self.is_image(imagen_path):
            return {
                "session_id": session_id,
                "funcionalidad": "error",
                "respuesta": {
                    "output": "❌ Formato de archivo no soportado. Solo se permiten imágenes.",
                    "metadata": {"tipo": "formato_no_soportado"}
                },
                "metadata": {"error": "Formato no soportado"}
            }

        # Clasificar automáticamente como análisis de imágenes
        funcionalidad = FuncionalidadMedica.ANALISIS_IMAGENES.key
        print(f"[ORQUESTADOR] Procesando imagen como: {funcionalidad}")

        agente = self.agentes.get(funcionalidad)
        if not agente:
            return {
                "session_id": session_id,
                "funcionalidad": funcionalidad,
                "respuesta": {
                    "output": "❌ Agente de análisis de imágenes no disponible",
                    "metadata": {"tipo": "error_agente"}
                },
                "metadata": {"error": "Agente no registrado"}
            }

        try:
            # Iniciar interacción si el método existe
            metadata = agente.iniciar_interaccion(session_id, imagen_path)

            # Procesar la imagen médica
            respuesta = agente.preguntar(
                session_id=session_id,
                pregunta=f"{mensaje}; Además adjunto una imagen, te pasare los resultados del análisis: {imagen_path}",
                metadata=metadata
            )

            return {
                "session_id": session_id,
                "funcionalidad": funcionalidad,
                "respuesta": respuesta,
                "metadata": metadata if metadata else {}
            }

        except Exception as e:
            error_msg = f"Error procesando imagen médica: {str(e)}"
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
        """
        funcionalidad = FuncionalidadMedica.INTERPRETACION_EXAMENES.key
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
        
