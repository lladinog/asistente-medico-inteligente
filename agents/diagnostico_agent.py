import json
from datetime import datetime
from app.config import COLORS

class DiagnosticoAgent:
    """Agente de inteligencia artificial para diagnóstico médico preliminar"""
    
    def __init__(self):
        self.sintomas_comunes = {
            "fiebre": ["gripe", "infección viral", "COVID-19", "infección bacteriana"],
            "dolor_cabeza": ["migraña", "tensión", "deshidratación", "fatiga visual"],
            "dolor_garganta": ["faringitis", "amigdalitis", "infección viral", "alergia"],
            "tos": ["resfriado", "bronquitis", "alergia", "asma"],
            "dolor_abdominal": ["gastritis", "indigestión", "apendicitis", "cólico"],
            "nausea": ["gastritis", "intoxicación", "migraña", "ansiedad"],
            "fatiga": ["anemia", "depresión", "hipotiroidismo", "estrés"],
            "dolor_articular": ["artritis", "esguince", "gota", "fibromialgia"]
        }
        
        self.prioridades = {
            "emergencia": ["dolor_pecho", "dificultad_respirar", "pérdida_conciencia", "sangrado_abundante"],
            "urgente": ["fiebre_alta", "dolor_severo", "trauma_reciente", "vómitos_persistentes"],
            "moderado": ["síntomas_leves", "malestar_general", "dolor_leve"],
            "leve": ["molestias_menores", "síntomas_transitorios"]
        }
    
    def analizar_sintomas(self, edad, sexo, sintomas, tiempo, intensidad):
        """
        Analiza los síntomas del paciente y genera un diagnóstico preliminar
        
        Args:
            edad (int): Edad del paciente
            sexo (str): Sexo del paciente (M/F/N)
            sintomas (str): Descripción de síntomas
            tiempo (str): Tiempo de evolución
            intensidad (int): Intensidad del malestar (1-10)
        
        Returns:
            dict: Diagnóstico preliminar con recomendaciones
        """
        # Normalizar síntomas
        sintomas_lower = sintomas.lower()
        
        # Detectar síntomas clave
        sintomas_detectados = []
        for sintoma, condiciones in self.sintomas_comunes.items():
            if sintoma.replace("_", " ") in sintomas_lower:
                sintomas_detectados.extend(condiciones)
        
        # Determinar prioridad
        prioridad = self._determinar_prioridad(sintomas_lower, intensidad)
        
        # Generar diagnóstico preliminar
        diagnostico = self._generar_diagnostico(sintomas_detectados, edad, sexo, tiempo, intensidad)
        
        # Generar recomendaciones
        recomendaciones = self._generar_recomendaciones(prioridad, sintomas_detectados, edad)
        
        return {
            "diagnostico": diagnostico,
            "prioridad": prioridad,
            "recomendaciones": recomendaciones,
            "sintomas_detectados": sintomas_detectados,
            "fecha_analisis": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
    
    def _determinar_prioridad(self, sintomas, intensidad):
        """Determina la prioridad del caso basado en síntomas e intensidad"""
        if any(sintoma in sintomas for sintoma in self.prioridades["emergencia"]):
            return "emergencia"
        elif any(sintoma in sintomas for sintoma in self.prioridades["urgente"]):
            return "urgente"
        elif intensidad >= 7:
            return "moderado"
        else:
            return "leve"
    
    def _generar_diagnostico(self, sintomas_detectados, edad, sexo, tiempo, intensidad):
        """Genera un diagnóstico preliminar basado en los síntomas detectados"""
        if not sintomas_detectados:
            return "Síntomas inespecíficos. Se requiere más información para un diagnóstico preliminar."
        
        # Tomar los síntomas más frecuentes
        sintomas_principales = list(set(sintomas_detectados))[:3]
        
        diagnostico = f"Basado en los síntomas descritos, las posibilidades diagnósticas incluyen: {', '.join(sintomas_principales)}. "
        
        if tiempo == "24h":
            diagnostico += "Los síntomas son de aparición reciente, lo que sugiere un proceso agudo. "
        elif tiempo in ["3d", "1w"]:
            diagnostico += "Los síntomas han persistido por varios días, requiriendo evaluación médica. "
        else:
            diagnostico += "Los síntomas de larga evolución requieren evaluación médica especializada. "
        
        if intensidad >= 8:
            diagnostico += "La intensidad de los síntomas es alta, recomendando atención médica pronta. "
        
        return diagnostico
    
    def _generar_recomendaciones(self, prioridad, sintomas_detectados, edad):
        """Genera recomendaciones específicas según la prioridad y síntomas"""
        recomendaciones = []
        
        if prioridad == "emergencia":
            recomendaciones.extend([
                "🚨 ACUDIR INMEDIATAMENTE A URGENCIAS",
                "📞 Llamar al servicio de emergencias local",
                "⚠️ No conducir si se siente mal"
            ])
        elif prioridad == "urgente":
            recomendaciones.extend([
                "🏥 Consultar con un médico en las próximas 24 horas",
                "📋 Llevar lista de síntomas y medicamentos actuales",
                "💊 No automedicarse sin supervisión médica"
            ])
        elif prioridad == "moderado":
            recomendaciones.extend([
                "👨‍⚕️ Programar consulta médica en los próximos días",
                "📝 Mantener registro de síntomas",
                "💧 Mantener hidratación adecuada",
                "😴 Descansar lo suficiente"
            ])
        else:
            recomendaciones.extend([
                "👀 Monitorear síntomas por 24-48 horas",
                "💊 Considerar medicamentos de venta libre si es apropiado",
                "🏠 Mantener reposo relativo",
                "📞 Consultar si los síntomas empeoran"
            ])
        
        # Recomendaciones específicas por síntomas
        if "fiebre" in str(sintomas_detectados).lower():
            recomendaciones.append("🌡️ Controlar temperatura regularmente")
        
        if "dolor" in str(sintomas_detectados).lower():
            recomendaciones.append("💊 Considerar analgésicos de venta libre")
        
        return recomendaciones
    
    def explicar_termino_medico(self, termino, nivel="intermedio"):
        """
        Explica un término médico en lenguaje sencillo
        
        Args:
            termino (str): Término médico a explicar
            nivel (str): Nivel de explicación (básico, intermedio, avanzado)
        
        Returns:
            dict: Explicación del término médico
        """
        terminos = {
            "hipertensión": {
                "básico": "Presión arterial alta que puede dañar el corazón y otros órganos",
                "intermedio": "Condición médica caracterizada por presión arterial persistentemente elevada (>140/90 mmHg)",
                "avanzado": "Trastorno cardiovascular crónico con múltiples factores etiológicos incluyendo genéticos, ambientales y de estilo de vida"
            },
            "diabetes": {
                "básico": "Enfermedad donde el cuerpo no puede controlar bien el azúcar en la sangre",
                "intermedio": "Trastorno metabólico caracterizado por hiperglucemia crónica debido a deficiencia de insulina o resistencia a la misma",
                "avanzado": "Síndrome metabólico complejo con múltiples manifestaciones sistémicas y complicaciones micro y macrovasculares"
            },
            "artritis": {
                "básico": "Inflamación de las articulaciones que causa dolor y rigidez",
                "intermedio": "Proceso inflamatorio articular que puede ser agudo o crónico, con múltiples etiologías",
                "avanzado": "Término general que engloba más de 100 condiciones reumáticas que afectan las articulaciones"
            }
        }
        
        termino_lower = termino.lower()
        if termino_lower in terminos:
            explicacion = terminos[termino_lower].get(nivel, terminos[termino_lower]["intermedio"])
        else:
            explicacion = f"El término '{termino}' se refiere a una condición médica específica. Para una explicación detallada, consulta con un profesional de la salud."
        
        return {
            "termino": termino,
            "nivel": nivel,
            "explicacion": explicacion,
            "recomendacion": "Esta explicación es informativa. Para diagnóstico y tratamiento, consulta con un médico."
        } 