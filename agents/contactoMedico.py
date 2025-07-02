import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, Dict
from dotenv import load_dotenv
from agents.agente import Agente
import json
import time

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
        
        # Datos del médico/centro médico
        self.datos_medico = {
            "nombre": "Dr. Juan Pérez",
            "especialidad": "Medicina Familiar",
            "centro": "Centro de Salud Urbano",
            "ubicacion": "Calle Principal #123",
            "telefono": "+57 (4) 123-4567",
            "horario": "Lunes a Viernes 8:00 AM - 6:00 PM"
        }
        
        # Estado de sesiones para manejo de flujo
        self.sesiones_estado = {}

    def iniciar_interaccion(self, session_id: str, mensaje: str) -> Dict:
        """Inicia la interacción y determina si necesita datos del paciente"""
        print(f"[CONTACTO_MEDICO] Iniciando interacción para sesión {session_id}")
        
        # Inicializar estado de sesión
        self.sesiones_estado[session_id] = {
            "paso": "recopilar_datos",
            "datos_recopilados": {},
            "mensaje_original": mensaje,
            "timestamp": time.time()
        }
        
        return {
            "accion": "recopilar_datos",
            "paso": "inicial",
            "mensaje": "Para contactar con el médico y generar un resumen de su caso, necesitamos algunos datos personales."
        }

    def preguntar(self, session_id: str, pregunta: str, metadata: Optional[Dict] = None) -> Dict:
        """Procesa las preguntas y maneja el flujo de recopilación de datos"""
        
        # Verificar si existe estado de sesión
        if session_id not in self.sesiones_estado:
            self.sesiones_estado[session_id] = {
                "paso": "generar_resumen",
                "datos_recopilados": {},
                "mensaje_original": pregunta,
                "timestamp": time.time()
            }
        
        estado_sesion = self.sesiones_estado[session_id]
        
        # Manejar diferentes pasos del flujo
        if metadata and metadata.get("accion") == "recopilar_datos":
            return self._manejar_recopilacion_datos(session_id, pregunta, metadata)
        
        elif metadata and metadata.get("accion") == "confirmar_envio":
            return self._confirmar_y_enviar(session_id, pregunta, metadata)
        
        else:
            return self._generar_resumen_medico(session_id, pregunta)

    def _manejar_recopilacion_datos(self, session_id: str, pregunta: str, metadata: Dict) -> Dict:
        """Maneja el proceso de recopilación de datos del paciente"""
        estado = self.sesiones_estado[session_id]
        paso = metadata.get("paso", "inicial")
        
        if paso == "inicial":
            return {
                "output": "📋 **Información del Paciente**\n\nPara generar un resumen médico adecuado, por favor proporcione:\n\n• Nombre completo\n• Edad\n• Número de teléfono de contacto\n• Descripción detallada de sus síntomas o motivo de consulta\n\nPuede escribir toda la información en un solo mensaje o paso a paso.",
                "metadata": {
                    "accion": "esperando_datos",
                    "paso": "recopilando",
                    "campos_requeridos": ["nombre", "edad", "telefono", "motivo"]
                }
            }
        
        elif paso == "recopilando":
            datos_extraidos = self._extraer_datos_paciente(pregunta)
            estado["datos_recopilados"].update(datos_extraidos)
            
            # Verificar si faltan datos
            campos_faltantes = self._verificar_datos_completos(estado["datos_recopilados"])
            
            if campos_faltantes:
                return {
                    "output": f"📝 Información recibida. Aún necesitamos:\n\n{self._formatear_campos_faltantes(campos_faltantes)}\n\nPor favor, proporcione la información faltante.",
                    "metadata": {
                        "accion": "esperando_datos",
                        "paso": "recopilando",
                        "campos_faltantes": campos_faltantes,
                        "datos_actuales": estado["datos_recopilados"]
                    }
                }
            else:
                # Datos completos, proceder a confirmación
                return self._mostrar_confirmacion(session_id)

    def _extraer_datos_paciente(self, texto: str) -> Dict:
        """Extrae datos del paciente usando procesamiento de texto con LLM"""
        # Crear prompt específico para extracción de datos
        prompt_extraccion = f"""
Extrae la siguiente información del texto del paciente. Si algún dato no está presente, no lo incluyas en la respuesta.

Texto del paciente: "{texto}"

Extrae SOLO la información que esté claramente presente:
- Nombre completo
- Edad (número)
- Teléfono (con formato)
- Motivo de consulta/síntomas

Responde en formato JSON válido únicamente con los campos encontrados.
"""
        
        try:
            # Usar el LLM para extraer información
            respuesta_llm = super().preguntar(
                session_id="extraccion_temp",
                pregunta=prompt_extraccion
            )
            
            # Intentar parsear la respuesta como JSON
            respuesta_texto = respuesta_llm.get("output", "").strip()
            
            import re
            json_match = re.search(r'\{.*\}', respuesta_texto, re.DOTALL)
            if json_match:
                datos = json.loads(json_match.group())
                return datos
            
        except Exception as e:
            print(f"[WARNING] Error en extracción automática: {e}")
        
        # Fallback: extracción manual básica
        return self._extraccion_manual_basica(texto)

    def _extraccion_manual_basica(self, texto: str) -> Dict:
        """Extracción básica usando expresiones regulares"""
        import re
        datos = {}
        
        # Extraer edad
        edad_match = re.search(r'\b(\d{1,3})\s*años?|\b(\d{1,3})\s*a[ñn]os?', texto.lower())
        if edad_match:
            datos["edad"] = edad_match.group(1) or edad_match.group(2)
        
        # Extraer teléfono
        tel_match = re.search(r'(\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4})', texto)
        if tel_match:
            datos["telefono"] = tel_match.group(1)
        
        # Si el texto es descriptivo y largo, probablemente es el motivo
        if len(texto.split()) > 5:
            datos["motivo"] = texto
            
        return datos

    def _verificar_datos_completos(self, datos: Dict) -> list:
        """Verifica qué campos faltan por completar"""
        campos_requeridos = ["nombre", "edad", "telefono", "motivo"]
        campos_faltantes = []
        
        for campo in campos_requeridos:
            if campo not in datos or not datos[campo]:
                campos_faltantes.append(campo)
        
        return campos_faltantes

    def _formatear_campos_faltantes(self, campos: list) -> str:
        """Formatea la lista de campos faltantes para mostrar al usuario"""
        nombres_campos = {
            "nombre": "• Nombre completo",
            "edad": "• Edad",
            "telefono": "• Teléfono de contacto",
            "motivo": "• Descripción de síntomas o motivo de consulta"
        }
        
        return "\n".join([nombres_campos.get(campo, f"• {campo}") for campo in campos])

    def _mostrar_confirmacion(self, session_id: str) -> Dict:
        """Muestra los datos recopilados para confirmación"""
        datos = self.sesiones_estado[session_id]["datos_recopilados"]
        
        resumen_datos = f"""
📋 **Confirmación de Datos**

**Paciente:** {datos.get('nombre', 'No especificado')}
**Edad:** {datos.get('edad', 'No especificada')} años
**Teléfono:** {datos.get('telefono', 'No especificado')}
**Motivo de consulta:** {datos.get('motivo', 'No especificado')}

**Médico asignado:** {self.datos_medico['nombre']} ({self.datos_medico['especialidad']})
**Centro:** {self.datos_medico['centro']}

¿Confirma que desea enviar esta información al médico? Responda 'sí' para confirmar o 'no' para cancelar.
"""
        
        return {
            "output": resumen_datos,
            "metadata": {
                "accion": "confirmar_envio",
                "datos_paciente": datos,
                "esperando_confirmacion": True
            }
        }

    def _confirmar_y_enviar(self, session_id: str, respuesta: str, metadata: Dict) -> Dict:
        """Procesa la confirmación y envía el caso al médico"""
        confirmacion = respuesta.lower().strip()
        
        if confirmacion in ['si', 'sí', 'yes', 'confirmar', 'confirmo', 'ok']:
            return self._enviar_caso_medico(session_id, metadata["datos_paciente"])
        
        elif confirmacion in ['no', 'cancelar', 'cancel']:
            
            if session_id in self.sesiones_estado:
                del self.sesiones_estado[session_id]
            
            return {
                "output": "❌ **Envío Cancelado**\n\nEl envío de su caso médico ha sido cancelado. Si desea intentar nuevamente, puede reiniciar el proceso.",
                "metadata": {
                    "accion": "cancelado",
                    "reiniciar": True
                }
            }
        
        else:
            return {
                "output": "⚠️ Por favor responda 'sí' para confirmar el envío o 'no' para cancelar.",
                "metadata": {
                    "accion": "confirmar_envio",
                    "datos_paciente": metadata["datos_paciente"],
                    "esperando_confirmacion": True
                }
            }

    def _enviar_caso_medico(self, session_id: str, datos_paciente: Dict) -> Dict:
        """Simula el envío del caso al médico y genera resumen"""
        resumen_medico = self._generar_resumen_estructurado(datos_paciente)
        
        numero_caso = f"CM-{int(time.time())}"
        
        if session_id in self.sesiones_estado:
            del self.sesiones_estado[session_id]
        
        return {
            "output": f"""
✅ **Caso Enviado Exitosamente**

**Número de caso:** {numero_caso}
**Estado:** Enviado para revisión médica

{resumen_medico}

---
📞 **Información de Contacto:**
**Médico:** {self.datos_medico['nombre']}
**Especialidad:** {self.datos_medico['especialidad']}
**Centro:** {self.datos_medico['centro']}
**Teléfono:** {self.datos_medico['telefono']}
**Horario:** {self.datos_medico['horario']}

⏰ **Tiempo estimado de respuesta:** 24-48 horas

El médico se pondrá en contacto con usted directamente en el teléfono proporcionado.
""",
            "metadata": {
                "accion": "enviado",
                "numero_caso": numero_caso,
                "datos_medico": self.datos_medico,
                "datos_paciente": datos_paciente,
                "timestamp": time.time()
            }
        }

    def _generar_resumen_medico(self, session_id: str, pregunta: str) -> Dict:
        """Genera un resumen médico cuando se hace una consulta directa"""
        prompt_resumen = f"""
Como asistente médico, genera un resumen profesional del siguiente caso para enviar a un médico:

Consulta del paciente: "{pregunta}"

Genera un resumen médico estructurado que incluya:
1. Motivo de consulta
2. Síntomas principales reportados
3. Información relevante mencionada
4. Recomendaciones para el médico

Mantén un tono profesional y médico.
"""
        
        try:
            respuesta_llm = super().preguntar(
                session_id=session_id,
                pregunta=prompt_resumen
            )
            
            resumen_generado = respuesta_llm.get("output", "")
            
            return {
                "output": f"""
📋 **Resumen Médico Generado**

{resumen_generado}

---
**Para enviar este caso a un médico para segunda opinión:**
- Responda 'enviar' si desea contactar con un médico
- O proporcione más detalles si es necesario

**Médico disponible:** {self.datos_medico['nombre']} ({self.datos_medico['especialidad']})
""",
                "metadata": {
                    "tipo": "resumen_generado",
                    "resumen": resumen_generado,
                    "puede_enviar": True
                }
            }
            
        except Exception as e:
            return {
                "output": f"❌ Error generando resumen médico: {str(e)}",
                "metadata": {
                    "tipo": "error",
                    "error": str(e)
                }
            }

    def _generar_resumen_estructurado(self, datos: Dict) -> str:
        """Genera un resumen médico estructurado para el médico"""
        return f"""
📋 **RESUMEN MÉDICO - CONSULTA REMOTA**

**Información del Paciente:**
• Nombre: {datos.get('nombre', 'No especificado')}
• Edad: {datos.get('edad', 'No especificada')} años
• Contacto: {datos.get('telefono', 'No especificado')}

**Motivo de Consulta:**
{datos.get('motivo', 'No especificado')}

**Fecha de solicitud:** {time.strftime('%Y-%m-%d %H:%M:%S')}
**Tipo de consulta:** Evaluación remota - Segunda opinión médica

**Nota:** Este caso requiere evaluación médica profesional para diagnóstico y tratamiento adecuado.
"""

    def limpiar_sesiones_expiradas(self, timeout_segundos: int = 3600):
        """Limpia sesiones que han expirado"""
        tiempo_actual = time.time()
        sesiones_expiradas = []
        
        for session_id, info in self.sesiones_estado.items():
            if tiempo_actual - info["timestamp"] > timeout_segundos:
                sesiones_expiradas.append(session_id)
        
        for session_id in sesiones_expiradas:
            del self.sesiones_estado[session_id]
            print(f"[CONTACTO_MEDICO] Sesión expirada limpiada: {session_id}")