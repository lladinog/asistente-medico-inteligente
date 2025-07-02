import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, Dict
from dotenv import load_dotenv

from agents.agente import Agente
from agents.exams import create_pdf_analysis_agent

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
            "n_ctx": int(os.getenv("LLAMA_N_CTX", 5000)),
            "temperature": 0.2,
            "max_tokens": 1024,
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
        
        # Inicializar el agente de análisis de PDFs
        self.pdf_agent = create_pdf_analysis_agent(model_config)
        self.pending_files = {}  # Para almacenar archivos pendientes por sesión
    
    def iniciar_interaccion(self, session_id: str, mensaje: str) -> Optional[Dict]:
        """Inicia la interacción con el agente de interpretación de exámenes"""
        print(f"[INTERPRETACION_EXAMENES] Iniciando interacción para sesión {session_id}")
        
        # Buscar si hay archivos PDF mencionados o pendientes
        metadata = {
            "tipo": "interpretacion_examenes",
            "session_id": session_id,
            "tiene_pdf_pendiente": session_id in self.pending_files,
            "archivos_soportados": self.pdf_agent.get_supported_formats()
        }
        
        return metadata
    
    def procesar_archivo_pdf(self, session_id: str, pdf_path: str, patient_context: str = "", patient_level: str = "intermedio") -> Dict:
        """
        Procesa un archivo PDF de examen médico
        
        Args:
            session_id: ID de la sesión
            pdf_path: Ruta al archivo PDF
            patient_context: Contexto del paciente
            patient_level: Nivel de explicación (simple/intermedio/detallado)
            
        Returns:
            Dict: Resultado del análisis del PDF
        """
        try:
            print(f"[INTERPRETACION_EXAMENES] Procesando PDF: {pdf_path}")
            
            # Procesar el PDF con el agente especializado
            resultado = self.pdf_agent.process_pdf_exam(
                pdf_path=pdf_path,
                patient_context=patient_context,
                patient_level=patient_level,
                session_id=session_id
            )
            
            if resultado.get("success"):
                # Almacenar el resultado para consultas posteriores
                self.pending_files[session_id] = resultado
                
                # Extraer información relevante para la respuesta
                classification = resultado.get("classification", {})
                medical_analysis = resultado.get("medical_analysis", {})
                patient_explanation = resultado.get("patient_explanation", "")
                
                return {
                    "output": self._formatear_respuesta_pdf(resultado),
                    "metadata": {
                        "tipo": "analisis_pdf_exitoso",
                        "analysis_id": resultado.get("analysis_id"),
                        "tipo_examen": classification.get("tipo_examen", "desconocido"),
                        "urgencia": medical_analysis.get("urgency_level", "NORMAL"),
                        "tiene_analisis_completo": True
                    }
                }
            else:
                error_msg = resultado.get("error", "Error desconocido procesando PDF")
                return {
                    "output": f"❌ **Error procesando el examen médico:**\n\n{error_msg}\n\nPor favor, verifica que el archivo sea un PDF válido con texto legible.",
                    "metadata": {
                        "tipo": "error_pdf",
                        "error": error_msg
                    }
                }
                
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            return {
                "output": f"❌ **Error procesando el archivo:**\n\n{error_msg}",
                "metadata": {
                    "tipo": "error_procesamiento",
                    "error": error_msg
                }
            }
    
    def preguntar(self, session_id: str, pregunta: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Procesa preguntas sobre exámenes médicos
        
        Args:
            session_id: ID de la sesión
            pregunta: Pregunta del usuario
            metadata: Metadatos adicionales (puede incluir info del archivo)
            
        Returns:
            Dict: Respuesta del agente
        """
        
        # Si hay metadatos de archivo PDF, procesarlo
        if metadata and metadata.get("pdf_path"):
            patient_context = metadata.get("patient_context", "")
            patient_level = metadata.get("patient_level", "intermedio")
            
            return self.procesar_archivo_pdf(
                session_id=session_id,
                pdf_path=metadata["pdf_path"],
                patient_context=patient_context,
                patient_level=patient_level
            )
        
        # Si hay un análisis previo en la sesión, usarlo como contexto
        if session_id in self.pending_files:
            resultado_previo = self.pending_files[session_id]
            contexto_analisis = self._extraer_contexto_analisis(resultado_previo)
            
            # Combinar la pregunta con el contexto del análisis
            pregunta_completa = f"""
CONTEXTO DEL ANÁLISIS PREVIO:
{contexto_analisis}

PREGUNTA DEL USUARIO:
{pregunta}

Por favor, responde la pregunta basándote en el análisis médico previo.
"""
            
            respuesta = super().preguntar(session_id, pregunta_completa, metadata)
            
            # Agregar metadatos indicando que se usó contexto previo
            if isinstance(respuesta, dict):
                respuesta["metadata"] = respuesta.get("metadata", {})
                respuesta["metadata"]["uso_contexto_previo"] = True
                respuesta["metadata"]["analysis_id"] = resultado_previo.get("analysis_id")
            
            return respuesta
        
        # Si no hay contexto de PDF, respuesta estándar
        return {
            "output": """📊 **Agente de Interpretación de Exámenes Médicos**

Para analizar un examen médico, puedes:

1. **Subir un archivo PDF** con los resultados de tu examen
2. **Proporcionar valores específicos** que quieras que interprete
3. **Hacer preguntas** sobre exámenes médicos en general

**Formatos soportados:** PDF

**Tipos de exámenes que puedo analizar:**
- Análisis de laboratorio (hemograma, química sanguínea, etc.)
- Estudios de imagen (radiografías, ecografías, etc.)
- Estudios funcionales
- Biopsias y patología
- Cualquier examen médico en formato PDF

¿Qué examen médico te gustaría que analice?""",
            "metadata": {"tipo": "instrucciones_uso"}
        }
    
    def _formatear_respuesta_pdf(self, resultado: Dict) -> str:
        """Formatea la respuesta del análisis de PDF para el usuario"""
        
        if not resultado.get("success"):
            return f"❌ Error en el análisis: {resultado.get('error', 'Error desconocido')}"
        
        classification = resultado.get("classification", {})
        medical_analysis = resultado.get("medical_analysis", {})
        patient_explanation = resultado.get("patient_explanation", "")
        
        tipo_examen = classification.get("tipo_examen", "Examen médico")
        urgencia = medical_analysis.get("urgency_level", "NORMAL")
        
        # Definir emoji según urgencia
        urgencia_emoji = {
            "NORMAL": "✅",
            "SEGUIMIENTO": "⚠️",
            "URGENTE": "🚨",
            "CRÍTICO": "🆘"
        }.get(urgencia, "📊")
        
        respuesta = f"""📋 **Análisis de Examen Médico Completado**

{urgencia_emoji} **Tipo de examen:** {tipo_examen.title()}
{urgencia_emoji} **Nivel de urgencia:** {urgencia}

---

## 📖 Explicación para el paciente:

{patient_explanation}

---

💡 **¿Tienes alguna pregunta específica sobre estos resultados?** 
Puedes preguntarme sobre cualquier valor, término médico o recomendación que no entiendas.
"""
        
        return respuesta
    
    def _extraer_contexto_analisis(self, resultado: Dict) -> str:
        """Extrae contexto relevante del análisis para preguntas posteriores"""
        
        classification = resultado.get("classification", {})
        medical_analysis = resultado.get("medical_analysis", {})
        
        contexto = f"""
Tipo de examen: {classification.get("tipo_examen", "desconocido")}
Nivel de urgencia: {medical_analysis.get("urgency_level", "NORMAL")}
Análisis médico: {medical_analysis.get("analysis", "No disponible")[:500]}...
"""
        
        return contexto
    
    def obtener_historial_analisis(self, session_id: str) -> Optional[Dict]:
        """Obtiene el historial de análisis para una sesión"""
        return self.pending_files.get(session_id)
    
    def limpiar_sesion(self, session_id: str):
        """Limpia los datos de una sesión específica"""
        if session_id in self.pending_files:
            del self.pending_files[session_id]
