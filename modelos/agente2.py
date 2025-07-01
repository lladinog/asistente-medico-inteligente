import sys
import os

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.llms import LlamaCpp
from agents.utils.conversation import Conversation
from modelos.medical_diagnosis_agent import MedicalDiagnosisAgent

os.environ["LLAMA_LOG_LEVEL"] = "WARN"  # Puede ser: "ERROR", "WARN", "INFO", "DEBUG"

class Agente:
    def __init__(self, config: dict, model_config: dict, system_prompt_path: str):
        self.config = config
        self.model_config = model_config

        self.medical_system = None
        if MedicalDiagnosisAgent:
            try:
                self.medical_system = MedicalDiagnosisAgent()
                print("✅ Sistema de diagnóstico médico avanzado inicializado")
            except Exception as e:
                print(f"⚠️ Error al inicializar sistema médico: {e}")
            
        with open(system_prompt_path, encoding="utf-8") as f:
            self.system_prompt = f.read()

        # === 1. Crear plantilla del prompt ===
        self.prompt_template = PromptTemplate(
            input_variables=["history", "input", "context"],
            template=(
                f"{self.system_prompt}\n\n"
                "CONTEXTO MÉDICO ADICIONAL:\n{context}\n\n"
                "HISTORIAL DE CONVERSACIÓN RECIENTE:\n{history}\n\n"
                "PACIENTE: {input}\n"
                "ASISTENTE MÉDICO:"
            ),
        )

        # === 2. Inicializar modelo ===
        self.llm = LlamaCpp(
            model_path=self.model_config.get("model_path"),
            n_ctx=model_config.get("n_ctx", 2048),
            n_threads=model_config.get("n_threads", 8),
            n_batch=model_config.get("n_batch", 512),
            temperature=model_config.get("temperature", 0.3),  # Menor temperatura para respuestas más consistentes
            max_tokens=model_config.get("max_tokens", 512),
            top_p=model_config.get("top_p", 0.9),
            repeat_penalty=model_config.get("repeat_penalty", 1.1),
            stop=["Paciente:", "PACIENTE:", "Usuario:", "USUARIO:", "Human:", "HUMAN:"],
            verbose=model_config.get("verbose", False),
        )

        # === 3. Construir cadena con historial ===
        self.chain = self.prompt_template | self.llm

        # === 4. Historial por sesión ===
        self.history_factory = lambda session_id: Conversation(
            file_path=f"historiales/session_{session_id}.json",
            max_tokens=self.model_config.get("n_ctx", 2048) - 512,  # Reservar espacio para respuesta
            buffer_extra=512
        )

        self.agente = RunnableWithMessageHistory(
            self.chain,
            get_session_history=self.history_factory,
            input_messages_key="input",
            history_messages_key="history",
        )

        # Contexto de sesión para mantener coherencia
        self.session_contexts = {}
    
    def _detect_medical_query_type(self, query: str) -> str:
        """Detecta el tipo de consulta médica"""
        query_lower = query.lower()
        
        # Patrones para diferentes tipos de consultas
        symptoms_patterns = [
            r'siento|tengo|me duele|dolor|síntoma|molestia|malestar',
            r'fiebre|tos|dolor de cabeza|náuseas|vómito|diarrea',
            r'cansancio|fatiga|mareo|debilidad'
        ]
        
        emergency_patterns = [
            r'emergencia|urgente|grave|severo|intenso',
            r'sangrado|hemorragia|inconsciencia|convulsión',
            r'dificultad para respirar|dolor en el pecho'
        ]
        
        explanation_patterns = [
            r'qué es|explica|significado|define',
            r'cómo funciona|para qué sirve'
        ]
        
        if any(re.search(pattern, query_lower) for pattern in emergency_patterns):
            return "emergency"
        elif any(re.search(pattern, query_lower) for pattern in symptoms_patterns):
            return "symptoms"
        elif any(re.search(pattern, query_lower) for pattern in explanation_patterns):
            return "explanation"
        else:
            return "general"

    def _get_medical_context(self, query: str, query_type: str, session_id: str) -> str:
        """Obtiene contexto médico relevante"""
        context_parts = []
        
        # Usar el sistema médico avanzado si está disponible
        if self.medical_system:
            try:
                if query_type == "symptoms":
                    # Análisis completo con el sistema avanzado
                    diagnosis_result = self.medical_system.analyze_symptoms(query)
                    if diagnosis_result.get("success"):
                        context_parts.append(f"ANÁLISIS MÉDICO AVANZADO:")
                        context_parts.append(f"- Nivel de urgencia: {diagnosis_result['diagnosis']['urgency_level']}")
                        context_parts.append(f"- Condiciones posibles: {', '.join(diagnosis_result['diagnosis']['possible_conditions'][:3])}")
                        if diagnosis_result['diagnosis']['red_flags']:
                            context_parts.append(f"- Señales de alarma detectadas: {', '.join(diagnosis_result['diagnosis']['red_flags'])}")
                
                elif query_type == "emergency":
                    context_parts.append("🚨 CONSULTA DE EMERGENCIA DETECTADA")
                    context_parts.append(self.medical_system.get_emergency_contacts())
                
                elif query_type == "explanation":
                    # Extraer el término a explicar
                    terms = re.findall(r'qué es (\w+)|explica (\w+)|significado de (\w+)', query.lower())
                    if terms:
                        term = next((t for t in terms[0] if t), "término médico")
                        explanation = self.medical_system.explain_medical_term(term)
                        context_parts.append(f"EXPLICACIÓN MÉDICA: {explanation.get('explanation', '')}")
                
            except Exception as e:
                context_parts.append(f"Sistema médico avanzado no disponible: {str(e)}")
        
        # Contexto de sesión
        if session_id in self.session_contexts:
            session_context = self.session_contexts[session_id]
            if session_context.get('patient_info'):
                context_parts.append(f"INFO DEL PACIENTE: {session_context['patient_info']}")
            if session_context.get('current_symptoms'):
                context_parts.append(f"SÍNTOMAS ACTUALES: {', '.join(session_context['current_symptoms'])}")
        
        # Consejos generales según el tipo
        if query_type == "symptoms":
            context_parts.append("RECORDATORIO: Pregunta sobre duración, intensidad y factores que mejoran/empeoran los síntomas.")
        elif query_type == "emergency":
            context_parts.append("PROTOCOLO: Priorizar derivación inmediata a servicios de emergencia.")
        
        return "\n".join(context_parts) if context_parts else "Consulta médica general."

    def _update_session_context(self, session_id: str, query: str, response: str):
        """Actualiza el contexto de la sesión"""
        if session_id not in self.session_contexts:
            self.session_contexts[session_id] = {
                'patient_info': {},
                'current_symptoms': [],
                'conversation_summary': [],
                'last_update': datetime.now().isoformat()
            }
        
        context = self.session_contexts[session_id]
        
        # Extraer información del paciente
        age_match = re.search(r'(\d+)\s*años?', query.lower())
        if age_match:
            context['patient_info']['edad'] = age_match.group(1)
        
        gender_match = re.search(r'(hombre|mujer|masculino|femenino)', query.lower())
        if gender_match:
            context['patient_info']['genero'] = gender_match.group(1)
        
        # Extraer síntomas mencionados
        symptom_keywords = ['dolor', 'fiebre', 'tos', 'náuseas', 'mareo', 'cansancio', 'malestar']
        for symptom in symptom_keywords:
            if symptom in query.lower() and symptom not in context['current_symptoms']:
                context['current_symptoms'].append(symptom)
        
        # Mantener resumen de conversación (últimas 3 interacciones)
        context['conversation_summary'].append({
            'query': query[:100] + "..." if len(query) > 100 else query,
            'response_type': self._detect_medical_query_type(query),
            'timestamp': datetime.now().isoformat()
        })
        
        # Mantener solo las últimas 3 interacciones
        context['conversation_summary'] = context['conversation_summary'][-3:]
        context['last_update'] = datetime.now().isoformat()

    def preguntar(self, session_id: str, pregunta: str) -> str:
        """Procesa una pregunta médica con análisis avanzado"""
        try:
            os.makedirs("historiales", exist_ok=True)
            
            # Detectar tipo de consulta
            query_type = self._detect_medical_query_type(pregunta)
            
            # Obtener contexto médico relevante
            medical_context = self._get_medical_context(pregunta, query_type, session_id)
            
            # Si es una consulta de síntomas y tenemos el sistema avanzado, usar respuesta híbrida
            if query_type == "symptoms" and self.medical_system:
                try:
                    # Obtener análisis del sistema avanzado
                    advanced_analysis = self.medical_system.chat_diagnosis(pregunta)
                    
                    # Combinar con respuesta del LLM para personalización
                    llm_response = self.agente.invoke(
                        {
                            "input": pregunta,
                            "context": medical_context
                        }, 
                        config={"configurable": {"session_id": session_id}}
                    )
                                        
                    # Actualizar contexto de sesión
                    self._update_session_context(session_id, pregunta, llm_response)
                    
                    return llm_response
                    
                except Exception as e:
                    print(f"Error en análisis avanzado: {e}")
                    # Fallback al LLM básico
            
            # Respuesta estándar con LLM
            respuesta = self.agente.invoke(
                {
                    "input": pregunta,
                    "context": medical_context
                }, 
                config={"configurable": {"session_id": session_id}}
            )
            
            # Limpiar respuesta
            respuesta_limpia = self._clean_response(respuesta)
            
            # Actualizar contexto de sesión
            self._update_session_context(session_id, pregunta, respuesta_limpia)
            
            return respuesta_limpia
            
        except Exception as e:
            error_msg = f"Error procesando consulta: {str(e)}"
            print(error_msg)
            return "Lo siento, hubo un error procesando tu consulta. Por favor, reformula tu pregunta o consulta con un profesional médico."

    def _clean_response(self, response: str) -> str:
        """Limpia la respuesta del LLM"""
        # Remover repeticiones
        lines = response.split('\n')
        unique_lines = []
        for line in lines:
            if line.strip() and line not in unique_lines:
                unique_lines.append(line)
        
        cleaned = '\n'.join(unique_lines)
        
        # Remover patrones problemáticos
        cleaned = re.sub(r'(Paciente:|PACIENTE:|Usuario:|USUARIO:).*', '', cleaned)
        cleaned = re.sub(r'\n\s*\n', '\n', cleaned)  # Múltiples líneas vacías
        
        return cleaned.strip()

    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Obtiene información de la sesión"""
        return self.session_contexts.get(session_id, {})

    def reset_session(self, session_id: str):
        """Reinicia una sesión específica"""
        if session_id in self.session_contexts:
            del self.session_contexts[session_id]
        
        # Limpiar historial de archivos
        history_file = f"historiales/session_{session_id}.json"
        if os.path.exists(history_file):
            os.remove(history_file)


if __name__ == "__main__":
    # === Cargar variables de entorno y rutas antes de crear la clase ===
    load_dotenv()
    
    model_config = {
        "model_path": os.getenv("MODEL_PATH", r"C:\Users\HP\Downloads\llama-2-7b-chat.Q4_K_M.gguf"),
        "n_threads": int(os.getenv("LLAMA_N_THREADS", os.cpu_count() or 8)),
        "n_batch": int(os.getenv("LLAMA_N_BATCH", 512)),
        "n_ctx": int(os.getenv("LLAMA_N_CTX", 2048)),
        "temperature": float(os.getenv("LLAMA_TEMPERATURE", 0.3)),
        "max_tokens": int(os.getenv("LLAMA_MAX_TOKENS", 512)),
        "top_p": float(os.getenv("LLAMA_TOP_P", 0.9)),
        "repeat_penalty": float(os.getenv("LLAMA_REPEAT_PENALTY", 1.1)),
        "verbose": os.getenv("LLAMA_VERBOSE", "false").lower() == "true"
    }
    
    config = {
        "nombre": "Agente Médico Avanzado",
        "tipo": "diagnóstico_integrado",
    }

    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "prompts",
        "sistema_prototipo.txt"
    )

    agenteMedico = Agente(config=config, model_config=model_config, system_prompt_path=prompt_path)
    session_id = input("ID de sesión (ej: 001): ").strip()
    while True:
            pregunta = input("\n👤 Paciente: ").strip()
            
            if pregunta.lower() in ("salir", "exit", "quit"):
                print("👋 Sesión terminada. ¡Cuídate!")
                break
            elif pregunta.lower() == "info":
                session_info = agenteMedico.get_session_info(session_id)
                print(f"📋 Información de sesión: {json.dumps(session_info, indent=2, ensure_ascii=False)}")
                continue
            elif pregunta.lower() == "reset":
                agenteMedico.reset_session(session_id)
                print("🔄 Sesión reiniciada")
                continue
            elif not pregunta:
                print("⚠️ Por favor, describe tus síntomas o haz tu consulta.")
                continue
            
            print("🤔 Analizando...")
            respuesta = agenteMedico.preguntar(session_id, pregunta)
            print(f"\n🏥 Dr. Asistente: {respuesta}")
            print("-" * 60)