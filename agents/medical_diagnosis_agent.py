#!/usr/bin/env python3
"""
Agente de diagnóstico médico avanzado
Integra el sistema de diagnóstico médico completo con la aplicación refactorizada
"""

import sys
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

# Agregar el directorio raíz al path para importar el sistema de diagnóstico
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.insert(0, root_dir)

# Importar el sistema de diagnóstico médico
from modelos.diagnostico import create_medical_system, DiagnosisResult, UrgencyLevel

class MedicalDiagnosisAgent:
    """Agente de diagnóstico médico avanzado que integra el sistema completo"""
    
    def __init__(self):
        """Inicializa el agente con el sistema de diagnóstico médico"""
        self.medical_system = create_medical_system()
        self.conversation_history = []
        
    def analyze_symptoms(self, symptoms_text: str, patient_info: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analiza síntomas usando el sistema médico avanzado
        
        Args:
            symptoms_text (str): Descripción de síntomas del paciente
            patient_info (dict, optional): Información del paciente (edad, sexo, etc.)
        
        Returns:
            dict: Resultado completo del análisis médico
        """
        try:
            # Procesar diagnóstico usando el sistema médico
            diagnosis_result = self.medical_system.process_diagnosis(symptoms_text)
            
            # Formatear respuesta para la aplicación
            formatted_response = self._format_diagnosis_for_app(diagnosis_result, patient_info)
            
            # Guardar en historial
            self._save_to_history(symptoms_text, diagnosis_result, patient_info)
            
            return formatted_response
            
        except Exception as e:
            return self._handle_error(f"Error en el análisis médico: {str(e)}")
    
    def chat_diagnosis(self, user_input: str) -> str:
        """
        Procesa consulta de chat usando el sistema médico
        
        Args:
            user_input (str): Entrada del usuario
            
        Returns:
            str: Respuesta formateada del sistema médico
        """
        try:
            return self.medical_system.chat_diagnosis(user_input)
        except Exception as e:
            return f"Error en el sistema de chat: {str(e)}"
    
    def explain_medical_term(self, term: str, level: str = "intermedio") -> Dict[str, Any]:
        """
        Explica términos médicos usando el sistema avanzado
        
        Args:
            term (str): Término médico a explicar
            level (str): Nivel de explicación (simple, intermedio, detallado)
            
        Returns:
            dict: Explicación del término médico
        """
        try:
            # Usar el sistema médico para explicaciones más completas
            explanation = self.medical_system.format_diagnosis_response(
                self.medical_system.process_diagnosis(f"explicar {term}")
            )
            
            return {
                "term": term,
                "level": level,
                "explanation": explanation,
                "timestamp": datetime.now().isoformat(),
                "source": "Sistema Médico Avanzado"
            }
        except Exception as e:
            return {
                "term": term,
                "level": level,
                "explanation": f"Error al procesar el término: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "source": "Sistema Médico Avanzado"
            }
    
    def get_health_tips(self) -> str:
        """Obtiene consejos de salud del sistema médico"""
        return self.medical_system.get_health_tips()
    
    def get_emergency_contacts(self) -> str:
        """Obtiene contactos de emergencia del sistema médico"""
        return self.medical_system.get_emergency_contacts()
    
    def get_symptom_guide(self) -> str:
        """Obtiene guía para describir síntomas"""
        return self.medical_system.get_symptom_checker_guide()
    
    def get_conversation_history(self) -> List[Dict]:
        """Obtiene el historial de conversaciones"""
        return self.medical_system.get_conversation_history()
    
    def reset_conversation(self):
        """Reinicia el historial de conversación"""
        self.medical_system.reset_conversation()
    
    def _format_diagnosis_for_app(self, diagnosis: DiagnosisResult, patient_info: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Formatea el resultado del diagnóstico para la aplicación Dash
        
        Args:
            diagnosis (DiagnosisResult): Resultado del diagnóstico médico
            patient_info (dict, optional): Información del paciente
            
        Returns:
            dict: Resultado formateado para la aplicación
        """
        urgency_emoji = {
            UrgencyLevel.EMERGENCY: "🚨",
            UrgencyLevel.URGENT: "⚠️", 
            UrgencyLevel.ROUTINE: "ℹ️",
            UrgencyLevel.FOLLOW_UP: "📅"
        }
        
        # Calcular barras de confianza
        confidence_bars = "█" * int(diagnosis.confidence_level * 10) + "░" * (10 - int(diagnosis.confidence_level * 10))
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "patient_info": patient_info,
            "diagnosis": {
                "possible_conditions": diagnosis.possible_conditions,
                "urgency_level": diagnosis.urgency_level.value,
                "urgency_emoji": urgency_emoji[diagnosis.urgency_level],
                "urgency_explanation": diagnosis.urgency_explanation,
                "recommendations": diagnosis.recommendations,
                "red_flags": diagnosis.red_flags,
                "confidence_level": diagnosis.confidence_level,
                "confidence_bars": confidence_bars,
                "follow_up_needed": diagnosis.follow_up_needed,
                "specialist_referral": diagnosis.specialist_referral
            },
            "formatted_response": self.medical_system.format_diagnosis_response(diagnosis),
            "source": "Sistema Médico Avanzado"
        }
    
    def _save_to_history(self, symptoms_text: str, diagnosis: DiagnosisResult, patient_info: Optional[Dict] = None):
        """Guarda la consulta en el historial"""
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "symptoms": symptoms_text,
            "patient_info": patient_info,
            "diagnosis": diagnosis,
            "source": "MedicalDiagnosisAgent"
        })
    
    def _handle_error(self, error_message: str) -> Dict[str, Any]:
        """Maneja errores del sistema médico"""
        return {
            "success": False,
            "error": error_message,
            "timestamp": datetime.now().isoformat(),
            "recommendation": "Consultar con un profesional médico inmediatamente",
            "source": "Sistema Médico Avanzado"
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Obtiene información del sistema médico"""
        return {
            "system_name": "Sistema de Diagnóstico Médico Avanzado",
            "version": "2.0",
            "features": [
                "Análisis de síntomas con NLP",
                "Evaluación de urgencia médica",
                "Identificación de condiciones posibles",
                "Detección de señales de alarma",
                "Generación de recomendaciones",
                "Cálculo de nivel de confianza",
                "Historial de conversaciones"
            ],
            "knowledge_base": "Base de conocimiento médico completa",
            "specialties": [
                "Respiratorio", "Cardiovascular", "Gastrointestinal",
                "Neurológico", "Dermatológico", "Musculoesquelético"
            ],
            "timestamp": datetime.now().isoformat()
        }

# Función para crear una instancia del agente
def create_medical_diagnosis_agent():
    """Crea y retorna una instancia del agente de diagnóstico médico"""
    return MedicalDiagnosisAgent() 