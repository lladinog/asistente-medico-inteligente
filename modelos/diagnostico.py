import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
import difflib
import unicodedata

class UrgencyLevel(Enum):
    EMERGENCY = "emergencia"
    URGENT = "urgente"
    ROUTINE = "rutina"
    FOLLOW_UP = "seguimiento"

@dataclass
class DiagnosisResult:
    possible_conditions: List[str]
    urgency_level: UrgencyLevel
    urgency_explanation: str
    recommendations: List[str]
    red_flags: List[str]
    confidence_level: float
    follow_up_needed: bool
    specialist_referral: Optional[str]

class MedicalKnowledgeBase:
    """Base de conocimiento médico completa y gratuita"""
    
    def __init__(self):
        self.medical_conditions = {
            # RESPIRATORIO
            "resfriado_comun": {
                "symptoms": ["tos", "estornudos", "congestión nasal", "dolor de garganta", "fatiga leve", "fiebre baja"],
                "urgency": "routine",
                "description": "Infección viral común del tracto respiratorio superior",
                "recommendations": ["Reposo", "Hidratación abundante", "Analgésicos de venta libre", "Gárgaras con agua tibia y sal"],
                "red_flags": [],
                "specialist": None,
                "duration": "7-10 días"
            },
            "gripe": {
                "symptoms": ["fiebre alta", "dolor muscular", "dolor de cabeza", "fatiga severa", "tos", "congestión"],
                "urgency": "urgent",
                "description": "Infección viral del sistema respiratorio",
                "recommendations": ["Reposo absoluto", "Antivirales si se inicia temprano", "Control de fiebre", "Hidratación"],
                "red_flags": ["dificultad respiratoria", "fiebre muy alta persistente"],
                "specialist": None,
                "duration": "1-2 semanas"
            },
            "neumonia": {
                "symptoms": ["fiebre alta", "tos con flema", "dolor en el pecho", "dificultad respiratoria", "fatiga extrema"],
                "urgency": "emergency",
                "description": "Infección pulmonar que puede ser grave",
                "recommendations": ["Atención médica inmediata", "Antibióticos", "Hospitalización si es severa"],
                "red_flags": ["dificultad respiratoria severa", "confusión", "labios azulados"],
                "specialist": "neumólogo",
                "duration": "2-3 semanas con tratamiento"
            },
            "bronquitis": {
                "symptoms": ["tos persistente", "flema", "fatiga", "dolor en el pecho leve", "fiebre baja"],
                "urgency": "urgent",
                "description": "Inflamación de los bronquios",
                "recommendations": ["Reposo", "Expectorantes", "Inhalaciones de vapor", "Evitar irritantes"],
                "red_flags": ["tos con sangre", "dificultad respiratoria"],
                "specialist": None,
                "duration": "2-3 semanas"
            },
            "asma": {
                "symptoms": ["dificultad respiratoria", "sibilancias", "tos seca", "opresión en el pecho"],
                "urgency": "urgent",
                "description": "Enfermedad crónica de las vías respiratorias",
                "recommendations": ["Broncodilatadores", "Evitar desencadenantes", "Plan de acción para asma"],
                "red_flags": ["crisis asmática severa", "incapacidad para hablar"],
                "specialist": "neumólogo",
                "duration": "crónica"
            },
            
            # CARDIOVASCULAR
            "hipertension": {
                "symptoms": ["dolor de cabeza", "mareos", "visión borrosa", "fatiga", "palpitaciones"],
                "urgency": "urgent",
                "description": "Presión arterial elevada",
                "recommendations": ["Medicamentos antihipertensivos", "Dieta baja en sodio", "Ejercicio regular", "Control de peso"],
                "red_flags": ["dolor de cabeza severo", "confusión", "dolor en el pecho"],
                "specialist": "cardiólogo",
                "duration": "crónica"
            },
            "infarto": {
                "symptoms": ["dolor intenso en el pecho", "dolor en brazo izquierdo", "sudoración", "náuseas", "dificultad respiratoria"],
                "urgency": "emergency",
                "description": "Ataque cardíaco - emergencia médica",
                "recommendations": ["Llamar emergencias inmediatamente", "Aspirina si no hay contraindicaciones", "No conducir"],
                "red_flags": ["dolor torácico intenso", "pérdida de conciencia", "sudoración profusa"],
                "specialist": "cardiólogo",
                "duration": "emergencia"
            },
            "arritmia": {
                "symptoms": ["palpitaciones", "mareos", "fatiga", "dolor en el pecho", "desmayos"],
                "urgency": "urgent",
                "description": "Ritmo cardíaco irregular",
                "recommendations": ["ECG", "Medicamentos antiarrítmicos", "Evitar estimulantes"],
                "red_flags": ["desmayos frecuentes", "dolor torácico", "dificultad respiratoria"],
                "specialist": "cardiólogo",
                "duration": "variable"
            },
            
            # GASTROINTESTINAL
            "gastritis": {
                "symptoms": ["dolor abdominal superior", "náuseas", "vómitos", "sensación de llenura", "acidez"],
                "urgency": "routine",
                "description": "Inflamación del revestimiento del estómago",
                "recommendations": ["Antiácidos", "Dieta blanda", "Evitar irritantes", "Comidas pequeñas frecuentes"],
                "red_flags": ["vómito con sangre", "dolor abdominal severo"],
                "specialist": "gastroenterólogo",
                "duration": "1-2 semanas"
            },
            "gastroenteritis": {
                "symptoms": ["diarrea", "vómitos", "dolor abdominal", "fiebre", "deshidratación"],
                "urgency": "urgent",
                "description": "Inflamación del estómago e intestinos",
                "recommendations": ["Hidratación", "Dieta líquida", "Probióticos", "Reposo"],
                "red_flags": ["deshidratación severa", "sangre en heces", "fiebre alta"],
                "specialist": None,
                "duration": "3-7 días"
            },
            "apendicitis": {
                "symptoms": ["dolor abdominal que inicia en el ombligo", "dolor en fosa ilíaca derecha", "fiebre", "náuseas", "vómitos"],
                "urgency": "emergency",
                "description": "Inflamación del apéndice - requiere cirugía",
                "recommendations": ["Cirugía de emergencia", "No comer ni beber", "Atención médica inmediata"],
                "red_flags": ["dolor abdominal severo", "fiebre alta", "rigidez abdominal"],
                "specialist": "cirujano",
                "duration": "emergencia"
            },
            
            # NEUROLÓGICO
            "migrana": {
                "symptoms": ["dolor de cabeza intenso", "náuseas", "vómitos", "sensibilidad a la luz", "sensibilidad al sonido"],
                "urgency": "urgent",
                "description": "Dolor de cabeza severo y recurrente",
                "recommendations": ["Analgésicos específicos", "Ambiente oscuro y silencioso", "Hidratación", "Identificar desencadenantes"],
                "red_flags": ["dolor de cabeza súbito y severo", "confusión", "fiebre"],
                "specialist": "neurólogo",
                "duration": "4-72 horas"
            },
            "cefalea_tension": {
                "symptoms": ["dolor de cabeza como banda", "tensión muscular", "estrés", "fatiga"],
                "urgency": "routine",
                "description": "Dolor de cabeza por tensión muscular",
                "recommendations": ["Analgésicos de venta libre", "Relajación", "Masaje", "Técnicas de manejo del estrés"],
                "red_flags": ["dolor súbito severo", "cambios en la visión"],
                "specialist": None,
                "duration": "30 minutos a 7 días"
            },
            "ictus": {
                "symptoms": ["debilidad facial", "dificultad para hablar", "parálisis", "confusión", "pérdida de coordinación"],
                "urgency": "emergency",
                "description": "Accidente cerebrovascular - emergencia médica",
                "recommendations": ["Llamar emergencias inmediatamente", "No dar medicamentos", "Mantener vías aéreas libres"],
                "red_flags": ["pérdida súbita de función", "alteración del habla", "parálisis"],
                "specialist": "neurólogo",
                "duration": "emergencia"
            },
            
            # DERMATOLÓGICO
            "dermatitis": {
                "symptoms": ["picazón", "enrojecimiento", "inflamación", "sequedad", "descamación"],
                "urgency": "routine",
                "description": "Inflamación de la piel",
                "recommendations": ["Cremas hidratantes", "Evitar irritantes", "Corticoides tópicos", "Antihistamínicos"],
                "red_flags": ["infección secundaria", "fiebre"],
                "specialist": "dermatólogo",
                "duration": "1-4 semanas"
            },
            "psoriasis": {
                "symptoms": ["placas rojas con escamas", "picazón", "dolor", "rigidez articular"],
                "urgency": "routine",
                "description": "Enfermedad autoinmune de la piel",
                "recommendations": ["Tratamientos tópicos", "Fototerapia", "Medicamentos sistémicos", "Hidratación"],
                "red_flags": ["artritis psoriásica", "infección"],
                "specialist": "dermatólogo",
                "duration": "crónica"
            },
            
            # MUSCULOESQUELÉTICO
            "artritis": {
                "symptoms": ["dolor articular", "rigidez", "inflamación", "limitación del movimiento", "fatiga"],
                "urgency": "routine",
                "description": "Inflamación de las articulaciones",
                "recommendations": ["Antiinflamatorios", "Fisioterapia", "Ejercicio moderado", "Compresas frías/calientes"],
                "red_flags": ["deformidad articular", "fiebre", "pérdida de función"],
                "specialist": "reumatólogo",
                "duration": "crónica"
            },
            "lumbalgia": {
                "symptoms": ["dolor en la espalda baja", "rigidez", "espasmos musculares", "limitación del movimiento"],
                "urgency": "routine",
                "description": "Dolor en la región lumbar",
                "recommendations": ["Reposo relativo", "Analgésicos", "Fisioterapia", "Ejercicios de fortalecimiento"],
                "red_flags": ["dolor irradiado a piernas", "pérdida de control de esfínteres", "debilidad"],
                "specialist": "traumatólogo",
                "duration": "1-6 semanas"
            },
            
            # ENDOCRINO
            "diabetes": {
                "symptoms": ["sed excesiva", "micción frecuente", "fatiga", "visión borrosa", "pérdida de peso"],
                "urgency": "urgent",
                "description": "Trastorno del metabolismo de la glucosa",
                "recommendations": ["Control de glucemia", "Dieta específica", "Medicamentos", "Ejercicio regular"],
                "red_flags": ["cetoacidosis", "hipoglucemia severa", "infecciones frecuentes"],
                "specialist": "endocrinólogo",
                "duration": "crónica"
            },
            "hipotiroidismo": {
                "symptoms": ["fatiga", "aumento de peso", "intolerancia al frío", "piel seca", "depresión"],
                "urgency": "routine",
                "description": "Función tiroidea disminuida",
                "recommendations": ["Hormona tiroidea", "Seguimiento regular", "Dieta equilibrada"],
                "red_flags": ["mixedema", "alteraciones cardíacas"],
                "specialist": "endocrinólogo",
                "duration": "crónica"
            }
        }
        
        # Síntomas de emergencia absoluta
        self.emergency_symptoms = {
            "dolor_toracico_severo", "dificultad_respiratoria_severa", "perdida_conciencia",
            "convulsiones", "sangrado_abundante", "paralisis", "confusion_severa",
            "dolor_abdominal_severo", "vomito_sangre", "perdida_vision_subita",
            "debilidad_facial_subita", "dificultad_hablar_subita"
        }
        
        # Mapeo de síntomas a condiciones
        self.symptom_to_conditions = self._build_symptom_mapping()
        
        # Sinónimos para normalización
        self.symptom_synonyms = {
            "fiebre": ["calentura", "temperatura", "febrícula"],
            "dolor_cabeza": ["cefalea", "jaqueca", "migraña"],
            "nauseas": ["ganas de vomitar", "mareo", "náusea"],
            "diarrea": ["evacuaciones líquidas", "deposiciones blandas"],
            "tos": ["tusir", "tos seca", "tos con flema"],
            "fatiga": ["cansancio", "agotamiento", "debilidad"],
            "mareos": ["vértigo", "inestabilidad", "mareo"],
            "dolor_pecho": ["dolor torácico", "opresión pecho"],
            "dificultad_respirar": ["disnea", "falta de aire", "ahogo"],
            "dolor_abdominal": ["dolor de estómago", "dolor de barriga", "dolor de vientre"],
            "dolor_garganta": ["dolor al tragar", "molestia garganta"],
            "congestion": ["nariz tapada", "congestión nasal"],
            "palpitaciones": ["latidos fuertes", "corazón acelerado"],
            "sudoracion": ["transpiración", "sudor excesivo"],
            "picazon": ["comezón", "prurito", "rascazón"],
            "hinchazon": ["inflamación", "edema", "hinchazón"],
            "dolor_muscular": ["mialgia", "dolor en músculos"],
            "rigidez": ["entumecimiento", "tirantez"],
            "vision_borrosa": ["vista borrosa", "visión nublada"],
            "perdida_peso": ["adelgazamiento", "pérdida de peso"],
            "sed_excesiva": ["mucha sed", "polidipsia"],
            "miccion_frecuente": ["orinar mucho", "poliuria"]
        }

    def _build_symptom_mapping(self) -> Dict[str, List[str]]:
        """Construye mapeo de síntomas a condiciones"""
        mapping = {}
        for condition, data in self.medical_conditions.items():
            for symptom in data["symptoms"]:
                symptom_key = self._normalize_text(symptom)
                if symptom_key not in mapping:
                    mapping[symptom_key] = []
                mapping[symptom_key].append(condition)
        return mapping

    def _normalize_text(self, text: str) -> str:
        """Normaliza texto para comparación"""
        text = unicodedata.normalize('NFD', text)
        text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
        return text.lower().replace(' ', '_').replace('-', '_')

class FreeMedicalDiagnosisSystem:
    """Sistema de diagnóstico médico completamente gratuito"""
    
    def __init__(self):
        self.knowledge_base = MedicalKnowledgeBase()
        self.conversation_history = []
        
    def extract_symptoms(self, text: str) -> List[str]:
        """Extrae síntomas del texto usando NLP básico"""
        normalized_text = self.knowledge_base._normalize_text(text)
        found_symptoms = []
        
        # Buscar síntomas directos
        for symptom in self.knowledge_base.symptom_to_conditions.keys():
            if symptom in normalized_text:
                found_symptoms.append(symptom)
        
        # Buscar sinónimos
        for main_symptom, synonyms in self.knowledge_base.symptom_synonyms.items():
            for synonym in synonyms:
                normalized_synonym = self.knowledge_base._normalize_text(synonym)
                if normalized_synonym in normalized_text:
                    found_symptoms.append(main_symptom)
        
        # Buscar patrones específicos
        patterns = {
            "dolor": r"dolor\s+(?:de|en)\s+(\w+)",
            "fiebre": r"fiebre|temperatura|calentura",
            "dificultad": r"dificultad\s+(?:para|al)\s+(\w+)",
            "perdida": r"pérdida\s+(?:de|del)\s+(\w+)",
            "problemas": r"problemas\s+(?:de|con|para)\s+(\w+)"
        }
        
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, normalized_text, re.IGNORECASE)
            for match in matches:
                symptom_key = f"{pattern_name}_{match}"
                found_symptoms.append(symptom_key)
        
        return list(set(found_symptoms))  # Eliminar duplicados

    def assess_urgency(self, symptoms: List[str], text: str) -> Tuple[UrgencyLevel, str]:
        """Evalúa el nivel de urgencia basado en síntomas"""
        normalized_text = self.knowledge_base._normalize_text(text)
        
        # Palabras clave de emergencia
        emergency_keywords = [
            "intenso", "severo", "insoportable", "terrible", "agudo",
            "subito", "repentino", "perdida", "paralisis", "convulsiones",
            "sangre", "desmayo", "confusion", "dificultad_respirar"
        ]
        
        # Verificar síntomas de emergencia
        for emergency_symptom in self.knowledge_base.emergency_symptoms:
            if emergency_symptom in normalized_text:
                return UrgencyLevel.EMERGENCY, f"Síntoma de emergencia detectado: {emergency_symptom.replace('_', ' ')}"
        
        # Verificar palabras clave de emergencia
        emergency_count = sum(1 for keyword in emergency_keywords if keyword in normalized_text)
        if emergency_count >= 2:
            return UrgencyLevel.EMERGENCY, "Múltiples indicadores de emergencia detectados"
        
        # Evaluar basado en condiciones posibles
        possible_conditions = self.find_possible_conditions(symptoms)
        urgency_levels = []
        
        for condition in possible_conditions:
            if condition in self.knowledge_base.medical_conditions:
                urgency = self.knowledge_base.medical_conditions[condition]["urgency"]
                urgency_levels.append(urgency)
        
        if "emergency" in urgency_levels:
            return UrgencyLevel.EMERGENCY, "Condición de emergencia identificada"
        elif "urgent" in urgency_levels:
            return UrgencyLevel.URGENT, "Condición que requiere atención médica pronta"
        elif "routine" in urgency_levels:
            return UrgencyLevel.ROUTINE, "Condición que puede ser evaluada en consulta regular"
        else:
            return UrgencyLevel.FOLLOW_UP, "Síntomas requieren seguimiento médico"

    def find_possible_conditions(self, symptoms: List[str]) -> List[str]:
        """Encuentra condiciones posibles basadas en síntomas"""
        condition_scores = {}
        
        for symptom in symptoms:
            if symptom in self.knowledge_base.symptom_to_conditions:
                for condition in self.knowledge_base.symptom_to_conditions[symptom]:
                    if condition not in condition_scores:
                        condition_scores[condition] = 0
                    condition_scores[condition] += 1
        
        # Ordenar por puntuación y tomar los más probables
        sorted_conditions = sorted(condition_scores.items(), key=lambda x: x[1], reverse=True)
        return [condition for condition, score in sorted_conditions[:5]]

    def generate_recommendations(self, conditions: List[str], urgency: UrgencyLevel) -> List[str]:
        """Genera recomendaciones basadas en condiciones y urgencia"""
        recommendations = []
        
        if urgency == UrgencyLevel.EMERGENCY:
            recommendations.extend([
                "🚨 Buscar atención médica de emergencia INMEDIATAMENTE",
                "Dirigirse al servicio de urgencias más cercano",
                "Llamar al número de emergencias local",
                "No conducir - pedir ayuda para transporte"
            ])
        
        # Recomendaciones específicas por condición
        for condition in conditions:
            if condition in self.knowledge_base.medical_conditions:
                condition_data = self.knowledge_base.medical_conditions[condition]
                recommendations.extend(condition_data["recommendations"])
        
        # Recomendaciones generales
        general_recommendations = [
            "Mantener registro de síntomas y su evolución",
            "Seguir las indicaciones médicas al pie de la letra",
            "No automedicarse sin supervisión médica",
            "Consultar con profesional médico para diagnóstico definitivo"
        ]
        
        recommendations.extend(general_recommendations)
        return list(set(recommendations)) 

    def identify_red_flags(self, symptoms: List[str], text: str) -> List[str]:
        """Identifica banderas rojas en los síntomas"""
        red_flags = []
        normalized_text = self.knowledge_base._normalize_text(text)
        
        general_red_flags = {
            "fiebre_alta": ["fiebre muy alta", "temperatura mayor a 39", "fiebre de 40"],
            "dolor_severo": ["dolor intenso", "dolor insoportable", "dolor severo"],
            "sangrado": ["sangre", "sangrado", "hemorragia"],
            "dificultad_respiratoria": ["no puedo respirar", "falta de aire severa", "ahogo"],
            "confusion": ["confundido", "desorientado", "no reconoce"],
            "perdida_conciencia": ["desmayo", "perdida de conocimiento", "inconsciente"],
            "paralisis": ["no puedo mover", "paralizado", "entumecido"],
            "convulsiones": ["convulsiones", "ataques", "espasmos"]
        }
        
        for flag_type, keywords in general_red_flags.items():
            for keyword in keywords:
                if self.knowledge_base._normalize_text(keyword) in normalized_text:
                    red_flags.append(flag_type.replace('_', ' ').title())
        
        possible_conditions = self.find_possible_conditions(symptoms)
        for condition in possible_conditions:
            if condition in self.knowledge_base.medical_conditions:
                condition_red_flags = self.knowledge_base.medical_conditions[condition]["red_flags"]
                red_flags.extend(condition_red_flags)
        
        return list(set(red_flags))

    def calculate_confidence(self, symptoms: List[str], conditions: List[str]) -> float:
        """Calcula nivel de confianza del diagnóstico"""
        if not symptoms or not conditions:
            return 0.1
        
        total_symptoms = len(symptoms)
        matched_symptoms = 0
        
        for condition in conditions:
            if condition in self.knowledge_base.medical_conditions:
                condition_symptoms = self.knowledge_base.medical_conditions[condition]["symptoms"]
                for symptom in symptoms:
                    if any(self.knowledge_base._normalize_text(cs) == symptom for cs in condition_symptoms):
                        matched_symptoms += 1
        
        # Calcular confianza basada en síntomas coincidentes
        confidence = min(matched_symptoms / total_symptoms, 1.0)
        
        # Ajustar por número de condiciones (más específico = más confianza)
        if len(conditions) == 1:
            confidence *= 1.2
        elif len(conditions) > 3:
            confidence *= 0.8
        
        return min(confidence, 0.95)  # Máximo 95% de confianza

    def determine_specialist(self, conditions: List[str]) -> Optional[str]:
        """Determina qué especialista se necesita"""
        specialists = []
        
        for condition in conditions:
            if condition in self.knowledge_base.medical_conditions:
                specialist = self.knowledge_base.medical_conditions[condition]["specialist"]
                if specialist:
                    specialists.append(specialist)
        
        if not specialists:
            return None
        
        # Retornar el especialista más común
        from collections import Counter
        specialist_counts = Counter(specialists)
        return specialist_counts.most_common(1)[0][0]

    def process_diagnosis(self, symptoms_text: str) -> DiagnosisResult:
        """Procesa el diagnóstico completo"""
        # Extraer síntomas
        symptoms = self.extract_symptoms(symptoms_text)
        
        # Encontrar condiciones posibles
        possible_conditions = self.find_possible_conditions(symptoms)
        
        # Evaluar urgencia
        urgency_level, urgency_explanation = self.assess_urgency(symptoms, symptoms_text)
        
        # Generar recomendaciones
        recommendations = self.generate_recommendations(possible_conditions, urgency_level)
        
        # Identificar banderas rojas
        red_flags = self.identify_red_flags(symptoms, symptoms_text)
        
        # Calcular confianza
        confidence = self.calculate_confidence(symptoms, possible_conditions)
        
        # Determinar especialista
        specialist = self.determine_specialist(possible_conditions)
        
        # Formatear nombres de condiciones
        formatted_conditions = []
        for condition in possible_conditions:
            if condition in self.knowledge_base.medical_conditions:
                # Convertir nombre de condición a formato legible
                readable_name = condition.replace('_', ' ').title()
                description = self.knowledge_base.medical_conditions[condition]["description"]
                formatted_conditions.append(f"{readable_name} - {description}")
        
        if not formatted_conditions:
            formatted_conditions = ["No se pudieron identificar condiciones específicas con los síntomas proporcionados"]
        
        result = DiagnosisResult(
            possible_conditions=formatted_conditions,
            urgency_level=urgency_level,
            urgency_explanation=urgency_explanation,
            recommendations=recommendations[:8],  # Limitar recomendaciones
            red_flags=red_flags,
            confidence_level=confidence,
            follow_up_needed=urgency_level != UrgencyLevel.EMERGENCY,
            specialist_referral=specialist
        )
        
        # Guardar en historial
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "symptoms": symptoms_text,
            "extracted_symptoms": symptoms,
            "diagnosis": result
        })
        
        return result

    def format_diagnosis_response(self, diagnosis: DiagnosisResult) -> str:
        """Formatea la respuesta del diagnóstico para el chat"""
        urgency_emoji = {
            UrgencyLevel.EMERGENCY: "🚨",
            UrgencyLevel.URGENT: "⚠️",
            UrgencyLevel.ROUTINE: "ℹ️",
            UrgencyLevel.FOLLOW_UP: "📅"
        }
        
        # Calcular barras de confianza
        confidence_bars = "█" * int(diagnosis.confidence_level * 10) + "░" * (10 - int(diagnosis.confidence_level * 10))
        
        response = f"""
{urgency_emoji[diagnosis.urgency_level]} **EVALUACIÓN MÉDICA PRELIMINAR**

**🔍 Posibles Condiciones Identificadas:**
{chr(10).join(f"• {condition}" for condition in diagnosis.possible_conditions)}

**🚨 Nivel de Urgencia:** {diagnosis.urgency_level.value.upper()}
**📋 Explicación:** {diagnosis.urgency_explanation}

**💡 Recomendaciones Principales:**
{chr(10).join(f"• {rec}" for rec in diagnosis.recommendations[:5])}

**⚠️ Señales de Alarma a Vigilar:**
{chr(10).join(f"• {flag}" for flag in diagnosis.red_flags) if diagnosis.red_flags else "• No se identificaron señales de alarma específicas"}

**👨‍⚕️ Especialista Recomendado:** {diagnosis.specialist_referral or 'Médico general'}
**📅 Seguimiento Necesario:** {'Sí' if diagnosis.follow_up_needed else 'No'}

**📊 Nivel de Confianza:** {diagnosis.confidence_level:.0%} {confidence_bars}

---
**⚠️ DESCARGO DE RESPONSABILIDAD MÉDICA:**
Esta evaluación es únicamente informativa y educativa. NO constituye un diagnóstico médico profesional ni reemplaza la consulta con un médico cualificado. Los síntomas pueden tener múltiples causas y solo un profesional médico puede realizar un diagnóstico definitivo mediante examen físico y pruebas apropiadas.

**🏥 En caso de emergencia, contacte inmediatamente:**
• Servicios de emergencia: 123 (Colombia)
• Diríjase al centro de salud más cercano
• No demore la atención médica profesional
"""
        return response

    def chat_diagnosis(self, user_input: str) -> str:
        """Función principal para el chat de diagnóstico"""
        try:
            # Validar entrada
            if len(user_input.strip()) < 10:
                return """
⚠️ **Información Insuficiente**

Para poder ayudarte mejor, por favor proporciona más detalles sobre tus síntomas:

• **¿Qué síntomas específicos tienes?**
• **¿Cuándo comenzaron?**
• **¿Qué tan intensos son del 1 al 10?**
• **¿Has tenido esto antes?**
• **¿Tomas algún medicamento?**

Ejemplo: "Tengo dolor de cabeza intenso desde ayer, con náuseas y sensibilidad a la luz"
"""
            
            # Procesar diagnóstico
            diagnosis = self.process_diagnosis(user_input)
            
            # Formatear respuesta
            response = self.format_diagnosis_response(diagnosis)
            
            return response
            
        except Exception as e:
            return f"""
🚨 **ERROR EN EL SISTEMA DE DIAGNÓSTICO**

Ha ocurrido un error técnico: {str(e)}

**⚠️ Recomendación Inmediata:**
Dado que no podemos procesar tu consulta correctamente, te recomendamos:

• **Consultar inmediatamente con un profesional médico**
• **Si es una emergencia, dirigirse al servicio de urgencias**
• **Llamar al 123 si estás en Colombia**

**No retrases la atención médica profesional.**
"""

    def get_health_tips(self) -> str:
        """Proporciona consejos generales de salud"""
        tips = [
            "🏃‍♂️ Mantén actividad física regular (30 min diarios)",
            "🥗 Consume una dieta equilibrada rica en frutas y verduras", 
            "💧 Bebe al menos 8 vasos de agua al día",
            "😴 Duerme 7-8 horas diarias de calidad",
            "🧘‍♀️ Practica técnicas de manejo del estrés",
            "🚭 Evita el tabaco y limita el alcohol",
            "🩺 Realiza chequeos médicos preventivos regulares",
            "🧼 Mantén buena higiene personal y lavado de manos",
            "☀️ Protégete del sol con protector solar",
            "🧠 Mantén tu mente activa con lectura y aprendizaje"
        ]
        
        return "\n".join(tips)

    def get_emergency_contacts(self) -> str:
        """Proporciona información de contactos de emergencia"""
        return """
🚨 **NÚMEROS DE EMERGENCIA IMPORTANTES**

**Colombia:**
• Emergencias generales: **123**
• Cruz Roja: **132**
• Bomberos: **119**
• Policía: **112**

**Emergencias Médicas - Cuándo Llamar:**
• Dolor de pecho intenso
• Dificultad severa para respirar
• Pérdida de conciencia
• Sangrado abundante
• Convulsiones
• Signos de accidente cerebrovascular
• Reacciones alérgicas severas
• Trauma grave

**⚠️ Ante la duda, siempre es mejor buscar ayuda médica profesional.**
"""

    def get_symptom_checker_guide(self) -> str:
        """Guía para usar el verificador de síntomas"""
        return """
📋 **GUÍA PARA DESCRIBIR TUS SÍNTOMAS**

**🔍 Información Importante a Incluir:**

**1. Síntomas Principales:**
• ¿Qué sientes exactamente?
• ¿Dónde lo sientes?

**2. Tiempo:**
• ¿Cuándo comenzó?
• ¿Es constante o va y viene?

**3. Intensidad:**
• Del 1 al 10, ¿qué tan fuerte es?
• ¿Interfiere con tus actividades?

**4. Factores Desencadenantes:**
• ¿Qué lo empeora?
• ¿Qué lo mejora?

**5. Síntomas Acompañantes:**
• ¿Tienes otros síntomas?
• ¿Fiebre, náuseas, mareos?

**6. Historial:**
• ¿Has tenido esto antes?
• ¿Tomas medicamentos?
• ¿Alergias conocidas?

**📝 Ejemplo de Descripción Completa:**
"Tengo dolor de cabeza intenso (8/10) en el lado derecho desde hace 2 días. Es punzante y empeora con la luz. También tengo náuseas y vomité una vez. Nunca me había dolido tan fuerte la cabeza."

**✅ Esto me ayuda a darte una evaluación más precisa y útil.**
"""

    def get_conversation_history(self) -> List[Dict]:
        """Obtiene el historial de conversaciones"""
        return self.conversation_history

    def reset_conversation(self):
        """Reinicia el historial de conversación"""
        self.conversation_history = []

# Función para crear una instancia del sistema
def create_medical_system():
    """Crea y retorna una instancia del sistema médico"""
    return FreeMedicalDiagnosisSystem()
