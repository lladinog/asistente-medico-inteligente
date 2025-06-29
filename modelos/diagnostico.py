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
            "epoc": {
                "symptoms": ["disnea progresiva", "tos crónica", "expectoración", "fatiga", "sibilancias"],
                "urgency": "urgent",
                "description": "Enfermedad pulmonar obstructiva crónica",
                "recommendations": ["Broncodilatadores", "Oxigenoterapia", "Rehabilitación pulmonar", "Dejar de fumar"],
                "red_flags": ["exacerbación aguda", "cianosis", "confusión"],
                "specialist": "neumólogo",
                "duration": "crónica"
            },
            "embolia_pulmonar": {
                "symptoms": ["dolor torácico súbito", "disnea", "tos con sangre", "taquicardia", "sudoración"],
                "urgency": "emergency",
                "description": "Obstrucción de arterias pulmonares por coágulo",
                "recommendations": ["Atención médica inmediata", "Anticoagulantes", "Oxigenoterapia"],
                "red_flags": ["colapso cardiovascular", "cianosis", "dolor torácico severo"],
                "specialist": "neumólogo",
                "duration": "emergencia"
            },
            "tuberculosis": {
                "symptoms": ["tos persistente", "expectoración con sangre", "fiebre vespertina", "sudores nocturnos", "pérdida de peso"],
                "urgency": "urgent",
                "description": "Infección bacteriana pulmonar",
                "recommendations": ["Tratamiento antituberculoso", "Aislamiento", "Seguimiento estricto"],
                "red_flags": ["hemoptisis", "fiebre persistente", "pérdida de peso severa"],
                "specialist": "neumólogo",
                "duration": "6-12 meses de tratamiento"
            },
            "sinusitis": {
                "symptoms": ["dolor facial", "congestión nasal", "secreción purulenta", "dolor de cabeza", "fiebre"],
                "urgency": "routine",
                "description": "Inflamación de los senos paranasales",
                "recommendations": ["Descongestionantes", "Irrigación nasal", "Antibióticos si es bacteriana"],
                "red_flags": ["dolor facial severo", "fiebre alta", "alteraciones visuales"],
                "specialist": "otorrinolaringólogo",
                "duration": "1-2 semanas"
            },
            "faringitis": {
                "symptoms": ["dolor de garganta", "dificultad para tragar", "fiebre", "ganglios inflamados", "enrojecimiento"],
                "urgency": "routine",
                "description": "Inflamación de la faringe",
                "recommendations": ["Analgésicos", "Gárgaras", "Hidratación", "Antibióticos si es bacteriana"],
                "red_flags": ["dificultad respiratoria", "babeo", "trismus"],
                "specialist": "otorrinolaringólogo",
                "duration": "5-7 días"
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
            "insuficiencia_cardiaca": {
                "symptoms": ["disnea", "edema en piernas", "fatiga", "tos nocturna", "palpitaciones"],
                "urgency": "urgent",
                "description": "Incapacidad del corazón para bombear eficientemente",
                "recommendations": ["Diuréticos", "IECA", "Beta-bloqueadores", "Restricción de sal"],
                "red_flags": ["disnea en reposo", "edema pulmonar", "confusión"],
                "specialist": "cardiólogo",
                "duration": "crónica"
            },
            "angina_pecho": {
                "symptoms": ["dolor torácico", "presión en el pecho", "dolor irradiado", "disnea", "sudoración"],
                "urgency": "urgent",
                "description": "Dolor torácico por isquemia miocárdica",
                "recommendations": ["Nitroglicerina", "Reposo", "Evaluación cardiológica", "Control factores de riesgo"],
                "red_flags": ["dolor en reposo", "duración prolongada", "cambio en patrón"],
                "specialist": "cardiólogo",
                "duration": "episódica"
            },
            "trombosis_venosa": {
                "symptoms": ["dolor en pierna", "hinchazón", "enrojecimiento", "calor local", "sensibilidad"],
                "urgency": "urgent",
                "description": "Formación de coágulo en vena profunda",
                "recommendations": ["Anticoagulantes", "Elevación de extremidad", "Medias compresivas"],
                "red_flags": ["disnea súbita", "dolor torácico", "hinchazón masiva"],
                "specialist": "angiólogo",
                "duration": "3-6 meses de tratamiento"
            },
            "pericarditis": {
                "symptoms": ["dolor torácico punzante", "fiebre", "fatiga", "tos seca", "dificultad respiratoria"],
                "urgency": "urgent",
                "description": "Inflamación del pericardio",
                "recommendations": ["Antiinflamatorios", "Colchicina", "Reposo", "Seguimiento ecocardiográfico"],
                "red_flags": ["taponamiento cardíaco", "derrame pericárdico", "hipotensión"],
                "specialist": "cardiólogo",
                "duration": "2-6 semanas"
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
            "ulcera_peptica": {
                "symptoms": ["dolor abdominal", "acidez", "náuseas", "pérdida de apetito", "pérdida de peso"],
                "urgency": "urgent",
                "description": "Lesión en mucosa gástrica o duodenal",
                "recommendations": ["Inhibidores bomba protones", "Antibióticos si H. pylori", "Evitar AINES"],
                "red_flags": ["hemorragia digestiva", "perforación", "obstrucción"],
                "specialist": "gastroenterólogo",
                "duration": "4-8 semanas"
            },
            "hepatitis": {
                "symptoms": ["ictericia", "fatiga", "dolor abdominal", "náuseas", "orina oscura"],
                "urgency": "urgent",
                "description": "Inflamación del hígado",
                "recommendations": ["Reposo", "Dieta especial", "Evitar alcohol", "Seguimiento hepático"],
                "red_flags": ["encefalopatía", "coagulopatía", "ascitis"],
                "specialist": "gastroenterólogo",
                "duration": "variable según tipo"
            },
            "colecistitis": {
                "symptoms": ["dolor en hipocondrio derecho", "fiebre", "náuseas", "vómitos", "ictericia"],
                "urgency": "urgent",
                "description": "Inflamación de la vesícula biliar",
                "recommendations": ["Antibióticos", "Analgésicos", "Cirugía si es necesaria"],
                "red_flags": ["peritonitis", "sepsis", "pancreatitis"],
                "specialist": "cirujano",
                "duration": "1-2 semanas"
            },
            "pancreatitis": {
                "symptoms": ["dolor abdominal intenso", "náuseas", "vómitos", "fiebre", "taquicardia"],
                "urgency": "emergency",
                "description": "Inflamación del páncreas",
                "recommendations": ["Hospitalización", "Ayuno", "Hidratación IV", "Control del dolor"],
                "red_flags": ["shock", "falla multiorgánica", "necrosis pancreática"],
                "specialist": "gastroenterólogo",
                "duration": "1-2 semanas"
            },
            "sindrome_intestino_irritable": {
                "symptoms": ["dolor abdominal", "cambios en hábito intestinal", "distensión", "gases", "moco en heces"],
                "urgency": "routine",
                "description": "Trastorno funcional intestinal",
                "recommendations": ["Dieta FODMAP", "Fibra", "Probióticos", "Manejo del estrés"],
                "red_flags": ["sangre en heces", "pérdida de peso", "fiebre"],
                "specialist": "gastroenterólogo",
                "duration": "crónica"
            },
            "enfermedad_inflamatoria_intestinal": {
                "symptoms": ["diarrea crónica", "sangre en heces", "dolor abdominal", "pérdida de peso", "fiebre"],
                "urgency": "urgent",
                "description": "Inflamación crónica del tracto digestivo",
                "recommendations": ["Inmunosupresores", "Corticoides", "Biológicos", "Cirugía si es necesaria"],
                "red_flags": ["obstrucción", "perforación", "hemorragia masiva"],
                "specialist": "gastroenterólogo",
                "duration": "crónica"
            },
            "hernia_hiatal": {
                "symptoms": ["acidez", "regurgitación", "dolor torácico", "disfagia", "tos"],
                "urgency": "routine",
                "description": "Protrusión del estómago hacia el tórax",
                "recommendations": ["Inhibidores bomba protones", "Dieta", "Evitar acostarse después de comer"],
                "red_flags": ["disfagia severa", "vómito persistente", "dolor torácico"],
                "specialist": "gastroenterólogo",
                "duration": "crónica"
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
            "epilepsia": {
                "symptoms": ["convulsiones", "pérdida de conciencia", "movimientos involuntarios", "confusión post-ictal"],
                "urgency": "urgent",
                "description": "Trastorno neurológico con convulsiones recurrentes",
                "recommendations": ["Anticonvulsivantes", "Evitar desencadenantes", "Protección durante crisis"],
                "red_flags": ["status epilepticus", "lesiones por caídas", "depresión respiratoria"],
                "specialist": "neurólogo",
                "duration": "crónica"
            },
            "parkinson": {
                "symptoms": ["temblor en reposo", "rigidez", "bradicinesia", "inestabilidad postural", "alteraciones de la marcha"],
                "urgency": "routine",
                "description": "Enfermedad neurodegenerativa",
                "recommendations": ["Levodopa", "Fisioterapia", "Terapia ocupacional", "Ejercicio"],
                "red_flags": ["caídas frecuentes", "disfagia", "demencia"],
                "specialist": "neurólogo",
                "duration": "crónica progresiva"
            },
            "alzheimer": {
                "symptoms": ["pérdida de memoria", "confusión", "desorientación", "cambios de personalidad", "dificultad para tareas"],
                "urgency": "routine",
                "description": "Demencia neurodegenerativa",
                "recommendations": ["Inhibidores colinesterasa", "Estimulación cognitiva", "Cuidado integral"],
                "red_flags": ["agitación severa", "síntomas psicóticos", "desnutrición"],
                "specialist": "neurólogo",
                "duration": "crónica progresiva"
            },
            "esclerosis_multiple": {
                "symptoms": ["fatiga", "debilidad", "alteraciones visuales", "espasticidad", "alteraciones cognitivas"],
                "urgency": "urgent",
                "description": "Enfermedad desmielinizante del SNC",
                "recommendations": ["Inmunomoduladores", "Corticoides en brotes", "Fisioterapia", "Sintomáticos"],
                "red_flags": ["neuritis óptica", "mielitis transversa", "deterioro cognitivo"],
                "specialist": "neurólogo",
                "duration": "crónica"
            },
            "neuropatia_periferica": {
                "symptoms": ["hormigueo", "entumecimiento", "dolor neuropático", "debilidad", "pérdida de reflejos"],
                "urgency": "routine",
                "description": "Disfunción de nervios periféricos",
                "recommendations": ["Tratamiento causa subyacente", "Analgésicos neuropáticos", "Fisioterapia"],
                "red_flags": ["debilidad progresiva", "dificultad respiratoria", "disautonomía"],
                "specialist": "neurólogo",
                "duration": "variable"
            },
            "meningitis": {
                "symptoms": ["fiebre alta", "dolor de cabeza severo", "rigidez de nuca", "fotofobia", "vómitos"],
                "urgency": "emergency",
                "description": "Inflamación de las meninges",
                "recommendations": ["Antibióticos IV inmediatos", "Corticoides", "Aislamiento", "Soporte vital"],
                "red_flags": ["petequias", "alteración conciencia", "convulsiones"],
                "specialist": "neurólogo",
                "duration": "emergencia"
            },
            "vertigo": {
                "symptoms": ["sensación de giro", "náuseas", "vómitos", "desequilibrio", "nistagmo"],
                "urgency": "routine",
                "description": "Trastorno del equilibrio",
                "recommendations": ["Maniobras de reposicionamiento", "Antivertiginosos", "Fisioterapia vestibular"],
                "red_flags": ["síntomas neurológicos", "cefalea severa", "hipoacusia"],
                "specialist": "otorrinolaringólogo",
                "duration": "días a semanas"
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
            "eczema": {
                "symptoms": ["piel seca", "picazón intensa", "enrojecimiento", "vesículas", "costras"],
                "urgency": "routine",
                "description": "Dermatitis atópica crónica",
                "recommendations": ["Hidratación constante", "Corticoides tópicos", "Evitar alérgenos"],
                "red_flags": ["infección bacteriana", "eczema herpético"],
                "specialist": "dermatólogo",
                "duration": "crónica"
            },
            "acne": {
                "symptoms": ["comedones", "pápulas", "pústulas", "nódulos", "cicatrices"],
                "urgency": "routine",
                "description": "Enfermedad inflamatoria del folículo pilosebáceo",
                "recommendations": ["Retinoides tópicos", "Antibióticos", "Cuidado de la piel"],
                "red_flags": ["acné quístico severo", "cicatrices permanentes"],
                "specialist": "dermatólogo",
                "duration": "meses a años"
            },
            "urticaria": {
                "symptoms": ["ronchas", "picazón intensa", "hinchazón", "enrojecimiento", "angioedema"],
                "urgency": "urgent",
                "description": "Reacción alérgica cutánea",
                "recommendations": ["Antihistamínicos", "Corticoides", "Evitar desencadenantes"],
                "red_flags": ["anafilaxia", "dificultad respiratoria", "hinchazón facial"],
                "specialist": "dermatólogo",
                "duration": "horas a días"
            },
            "celulitis": {
                "symptoms": ["enrojecimiento", "hinchazón", "calor", "dolor", "fiebre"],
                "urgency": "urgent",
                "description": "Infección bacteriana de tejidos blandos",
                "recommendations": ["Antibióticos", "Elevación", "Analgésicos", "Seguimiento estrecho"],
                "red_flags": ["sepsis", "necrosis", "fascitis necrotizante"],
                "specialist": "dermatólogo",
                "duration": "1-2 semanas"
            },
            "herpes_zoster": {
                "symptoms": ["dolor punzante", "vesículas", "distribución dermatómica", "fiebre", "malestar"],
                "urgency": "urgent",
                "description": "Reactivación del virus varicela-zóster",
                "recommendations": ["Antivirales", "Analgésicos", "Cuidado local", "Aislamiento"],
                "red_flags": ["afectación ocular", "neuralgia post-herpética", "diseminación"],
                "specialist": "dermatólogo",
                "duration": "2-4 semanas"
            },
            "melanoma": {
                "symptoms": ["lunar asimétrico", "bordes irregulares", "cambio de color", "diámetro >6mm", "evolución"],
                "urgency": "urgent",
                "description": "Cáncer de piel maligno",
                "recommendations": ["Biopsia inmediata", "Extirpación quirúrgica", "Estudio extensión"],
                "red_flags": ["ulceración", "sangrado", "crecimiento rápido"],
                "specialist": "dermatólogo",
                "duration": "requiere tratamiento inmediato"
            },
            "vitiligo": {
                "symptoms": ["manchas blancas", "despigmentación", "distribución simétrica", "progresión"],
                "urgency": "routine",
                "description": "Trastorno autoinmune de la pigmentación",
                "recommendations": ["Corticoides tópicos", "Inhibidores calcineurina", "Fototerapia"],
                "red_flags": ["progresión rápida", "afectación extensa"],
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
            "artritis_reumatoidea": {
                "symptoms": ["dolor articular simétrico", "rigidez matutina", "inflamación", "fatiga", "fiebre"],
                "urgency": "urgent",
                "description": "Enfermedad autoinmune articular",
                "recommendations": ["DMARDs", "Metotrexato", "Biológicos", "Fisioterapia"],
                "red_flags": ["vasculitis", "nódulos reumatoideos", "afectación sistémica"],
                "specialist": "reumatólogo",
                "duration": "crónica"
            },
            "osteoporosis": {
                "symptoms": ["fracturas por fragilidad", "dolor óseo", "pérdida de altura", "cifosis"],
                "urgency": "routine",
                "description": "Disminución de la densidad ósea",
                "recommendations": ["Bifosfonatos", "Calcio", "Vitamina D", "Ejercicio con peso"],
                "red_flags": ["fracturas vertebrales", "fractura de cadera"],
                "specialist": "reumatólogo",
                "duration": "crónica"
            },
            "fibromialgia": {
                "symptoms": ["dolor generalizado", "fatiga", "alteraciones del sueño", "puntos sensibles", "rigidez"],
                "urgency": "routine",
                "description": "Síndrome de dolor crónico",
                "recommendations": ["Antidepresivos", "Pregabalina", "Ejercicio suave", "Terapia cognitiva"],
                "red_flags": ["depresión severa", "ideación suicida"],
                "specialist": "reumatólogo",
                "duration": "crónica"
            },
            "gota": {
                "symptoms": ["dolor articular intenso", "inflamación", "enrojecimiento", "calor", "inicio súbito"],
                "urgency": "urgent",
                "description": "Artritis por cristales de ácido úrico",
                "recommendations": ["Colchicina", "AINES", "Alopurinol", "Dieta baja en purinas"],
                "red_flags": ["afectación poliarticular", "fiebre", "tofos"],
                "specialist": "reumatólogo",
                "duration": "ataques agudos 3-10 días"
            },
            "hernia_discal": {
                "symptoms": ["dolor lumbar", "ciática", "entumecimiento", "debilidad en piernas", "parestesias"],
                "urgency": "urgent",
                "description": "Protrusión del disco intervertebral",
                "recommendations": ["Analgésicos", "Relajantes musculares", "Fisioterapia", "Cirugía si es severa"],
                "red_flags": ["síndrome cauda equina", "déficit neurológico", "incontinencia"],
                "specialist": "traumatólogo",
                "duration": "6-12 semanas"
            },
            "tendinitis": {
                "symptoms": ["dolor al movimiento", "sensibilidad", "rigidez", "inflamación leve", "crepitación"],
                "urgency": "routine",
                "description": "Inflamación de tendón",
                "recommendations": ["Reposo", "Hielo", "Antiinflamatorios", "Fisioterapia"],
                "red_flags": ["ruptura tendinosa", "infección", "dolor severo"],
                "specialist": "traumatólogo",
                "duration": "2-6 semanas"
            },
            "esguince": {
                "symptoms": ["dolor", "hinchazón", "hematoma", "limitación funcional", "inestabilidad"],
                "urgency": "routine",
                "description": "Lesión ligamentaria",
                "recommendations": ["RICE", "Vendaje", "Fisioterapia", "Rehabilitación gradual"],
                "red_flags": ["ruptura completa", "fractura asociada", "compromiso vascular"],
                "specialist": "traumatólogo",
                "duration": "2-8 semanas"
            },
            "fractura": {
                "symptoms": ["dolor intenso", "deformidad", "hinchazón", "hematoma", "impotencia funcional"],
                "urgency": "emergency",
                "description": "Rotura ósea",
                "recommendations": ["Inmovilización", "Analgésicos", "Reducción", "Fijación"],
                "red_flags": ["fractura expuesta", "compromiso vascular", "síndrome compartimental"],
                "specialist": "traumatólogo",
                "duration": "6-12 semanas"
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
            },
            "hipertiroidismo": {
                "symptoms": ["pérdida de peso", "palpitaciones", "sudoración", "nerviosismo", "temblor"],
                "urgency": "urgent",
                "description": "Función tiroidea aumentada",
                "recommendations": ["Antitiroideos", "Beta-bloqueadores", "Yodo radioactivo", "Cirugía"],
                "red_flags": ["tormenta tiroidea", "fibrilación auricular", "insuficiencia cardíaca"],
                "specialist": "endocrinólogo",
                "duration": "meses a años"
            },
            "sindrome_cushing": {
                "symptoms": ["aumento de peso central", "estrías púrpuras", "cara de luna", "hipertensión", "debilidad"],
                "urgency": "routine",
                "description": "Exceso de cortisol",
                "recommendations": ["Tratamiento causa subyacente", "Control metabólico", "Cirugía si tumor"],
                "red_flags": ["diabetes", "osteoporosis", "psicosis"],
                "specialist": "endocrinólogo",
                "duration": "variable"
            },
            "addison": {
                "symptoms": ["fatiga", "pérdida de peso", "hipotensión", "hiperpigmentación", "náuseas"],
                "urgency": "urgent",
                "description": "Insuficiencia suprarrenal",
                "recommendations": ["Corticoides", "Mineralocorticoides", "Educación paciente"],
                "red_flags": ["crisis addisoniana", "shock", "hipoglucemia"],
                "specialist": "endocrinólogo",
                "duration": "crónica"
            },
            "diabetes_insipida": {
                "symptoms": ["poliuria", "polidipsia", "nicturia", "deshidratación", "hipernatremia"],
                "urgency": "urgent",
                "description": "Deficiencia de ADH",
                "recommendations": ["Desmopresina", "Hidratación", "Control electrolitos"],
                "red_flags": ["deshidratación severa", "alteraciones neurológicas"],
                "specialist": "endocrinólogo",
                "duration": "variable"
            },
            
            # GENITOURINARIO
            "infeccion_urinaria": {
                "symptoms": ["disuria", "frecuencia urinaria", "urgencia", "dolor suprapúbico", "orina turbia"],
                "urgency": "routine",
                "description": "Infección del tracto urinario",
                "recommendations": ["Antibióticos", "Hidratación abundante", "Analgésicos", "Seguimiento"],
                "red_flags": ["fiebre", "dolor lumbar", "náuseas"],
                "specialist": "urólogo",
                "duration": "3-7 días"
            },
            "pielonefritis": {
                "symptoms": ["fiebre alta", "dolor lumbar", "náuseas", "vómitos", "disuria"],
                "urgency": "urgent",
                "description": "Infección renal",
                "recommendations": ["Antibióticos IV", "Hospitalización", "Hidratación", "Control imaging"],
                "red_flags": ["sepsis", "absceso renal", "insuficiencia renal"],
                "specialist": "urólogo",
                "duration": "1-2 semanas"
            },
            "litiasis_renal": {
                "symptoms": ["dolor cólico intenso", "hematuria", "náuseas", "vómitos", "disuria"],
                "urgency": "urgent",
                "description": "Cálculos en el riñón",
                "recommendations": ["Analgésicos potentes", "Hidratación", "Litotripsia", "Cirugía si necesario"],
                "red_flags": ["anuria", "fiebre", "insuficiencia renal"],
                "specialist": "urólogo",
                "duration": "días a semanas"
            },
            "insuficiencia_renal": {
                "symptoms": ["oliguria", "edema", "fatiga", "náuseas", "alteraciones electrolíticas"],
                "urgency": "urgent",
                "description": "Pérdida de función renal",
                "recommendations": ["Diálisis", "Control líquidos", "Dieta especial", "Tratamiento causa"],
                "red_flags": ["uremia", "edema pulmonar", "hiperpotasemia"],
                "specialist": "nefrólogo",
                "duration": "variable"
            },
            "prostatitis": {
                "symptoms": ["dolor pélvico", "disuria", "frecuencia", "fiebre", "dolor perineal"],
                "urgency": "urgent",
                "description": "Inflamación de la próstata",
                "recommendations": ["Antibióticos", "Alfabloqueadores", "Analgésicos", "Sitz baths"],
                "red_flags": ["retención urinaria", "sepsis", "absceso"],
                "specialist": "urólogo",
                "duration": "4-6 semanas"
            },
            "hiperplasia_prostatica": {
                "symptoms": ["chorro débil", "frecuencia", "nicturia", "goteo terminal", "sensación vaciado incompleto"],
                "urgency": "routine",
                "description": "Crecimiento benigno de próstata",
                "recommendations": ["Alfabloqueadores", "Inhibidores 5-alfa reductasa", "Cirugía"],
                "red_flags": ["retención urinaria", "hematuria", "infecciones recurrentes"],
                "specialist": "urólogo",
                "duration": "crónica progresiva"
            },
            "cistitis": {
                "symptoms": ["disuria", "urgencia", "frecuencia", "dolor suprapúbico", "hematuria"],
                "urgency": "routine",
                "description": "Inflamación de la vejiga",
                "recommendations": ["Antibióticos", "Hidratación", "Analgésicos", "Medidas higiénicas"],
                "red_flags": ["fiebre", "dolor lumbar", "hematuria macroscópica"],
                "specialist": None,
                "duration": "3-5 días"
            },
            
            # GINECOLÓGICO
            "vaginitis": {
                "symptoms": ["flujo vaginal", "picazón", "ardor", "dispareunia", "olor"],
                "urgency": "routine",
                "description": "Inflamación vaginal",
                "recommendations": ["Antifúngicos", "Antibióticos según causa", "Probióticos"],
                "red_flags": ["fiebre", "dolor pélvico", "sangrado"],
                "specialist": "ginecólogo",
                "duration": "1-2 semanas"
            },
            "endometriosis": {
                "symptoms": ["dismenorrea", "dispareunia", "dolor pélvico crónico", "infertilidad", "sangrado anormal"],
                "urgency": "routine",
                "description": "Tejido endometrial fuera del útero",
                "recommendations": ["Analgésicos", "Hormonoterapia", "Cirugía laparoscópica"],
                "red_flags": ["masa anexial", "dolor severo", "infertilidad"],
                "specialist": "ginecólogo",
                "duration": "crónica"
            },
            "miomas_uterinos": {
                "symptoms": ["menorragia", "dolor pélvico", "masa abdominal", "síntomas compresivos"],
                "urgency": "routine",
                "description": "Tumores benignos del útero",
                "recommendations": ["Observación", "Hormonoterapia", "Cirugía", "Embolización"],
                "red_flags": ["anemia severa", "crecimiento rápido", "torsión"],
                "specialist": "ginecólogo",
                "duration": "variable"
            },
            "ovarios_poliquisticos": {
                "symptoms": ["irregularidades menstruales", "hirsutismo", "acné", "obesidad", "infertilidad"],
                "urgency": "routine",
                "description": "Síndrome endocrino-metabólico",
                "recommendations": ["Metformina", "Anticonceptivos", "Antiandrogénicos", "Cambios estilo vida"],
                "red_flags": ["diabetes", "síndrome metabólico", "cáncer endometrial"],
                "specialist": "ginecólogo",
                "duration": "crónica"
            },
            
            # OFTALMOLÓGICO
            "conjuntivitis": {
                "symptoms": ["ojo rojo", "secreción", "picazón", "sensación cuerpo extraño", "lagrimeo"],
                "urgency": "routine",
                "description": "Inflamación de la conjuntiva",
                "recommendations": ["Lágrimas artificiales", "Antibióticos si bacteriana", "Antihistamínicos"],
                "red_flags": ["dolor severo", "pérdida visión", "fotofobia"],
                "specialist": "oftalmólogo",
                "duration": "1-2 semanas"
            },
            "glaucoma": {
                "symptoms": ["pérdida campo visual", "dolor ocular", "halos", "náuseas", "visión borrosa"],
                "urgency": "urgent",
                "description": "Aumento presión intraocular",
                "recommendations": ["Gotas hipotensoras", "Cirugía", "Seguimiento regular"],
                "red_flags": ["glaucoma agudo", "pérdida visual súbita", "dolor severo"],
                "specialist": "oftalmólogo",
                "duration": "crónica"
            },
            "cataratas": {
                "symptoms": ["visión borrosa", "deslumbramiento", "cambios refracción", "diplopía monocular"],
                "urgency": "routine",
                "description": "Opacidad del cristalino",
                "recommendations": ["Cirugía cuando interfiere visión", "Lentes correctores temporales"],
                "red_flags": ["pérdida visual significativa", "glaucoma secundario"],
                "specialist": "oftalmólogo",
                "duration": "progresiva"
            },
            "retinopatia_diabetica": {
                "symptoms": ["visión borrosa", "manchas visuales", "pérdida visual", "moscas volantes"],
                "urgency": "urgent",
                "description": "Complicación ocular de diabetes",
                "recommendations": ["Control glucémico", "Láser", "Inyecciones intravítreas"],
                "red_flags": ["hemorragia vítrea", "desprendimiento retina", "neovascularización"],
                "specialist": "oftalmólogo",
                "duration": "crónica progresiva"
            },
            "degeneracion_macular": {
                "symptoms": ["pérdida visión central", "metamorfopsia", "escotomas", "dificultad lectura"],
                "urgency": "urgent",
                "description": "Degeneración de la mácula",
                "recommendations": ["Inyecciones anti-VEGF", "Vitaminas", "Magnificación"],
                "red_flags": ["pérdida visual súbita", "hemorragia", "exudación"],
                "specialist": "oftalmólogo",
                "duration": "crónica progresiva"
            },
            
            # OTORRINOLARINGOLÓGICO
            "otitis_media": {
                "symptoms": ["dolor de oído", "fiebre", "hipoacusia", "secreción", "irritabilidad"],
                "urgency": "routine",
                "description": "Infección del oído medio",
                "recommendations": ["Antibióticos", "Analgésicos", "Descongestionantes"],
                "red_flags": ["mastoiditis", "meningitis", "parálisis facial"],
                "specialist": "otorrinolaringólogo",
                "duration": "1-2 semanas"
            },
            "hipoacusia": {
                "symptoms": ["pérdida auditiva", "tinnitus", "sensación plenitud", "dificultad comunicación"],
                "urgency": "routine",
                "description": "Disminución de la audición",
                "recommendations": ["Audífonos", "Implantes", "Tratamiento causa subyacente"],
                "red_flags": ["hipoacusia súbita", "asimetría", "síntomas neurológicos"],
                "specialist": "otorrinolaringólogo",
                "duration": "variable"
            },
            "rinitis_alergica": {
                "symptoms": ["estornudos", "rinorrea", "congestión", "picazón nasal", "lagrimeo"],
                "urgency": "routine",
                "description": "Inflamación alérgica de la nariz",
                "recommendations": ["Antihistamínicos", "Corticoides nasales", "Evitar alérgenos"],
                "red_flags": ["asma asociada", "sinusitis", "pólipos"],
                "specialist": "otorrinolaringólogo",
                "duration": "estacional o crónica"
            },
            "laringitis": {
                "symptoms": ["disfonía", "tos seca", "dolor garganta", "carraspeo", "fatiga vocal"],
                "urgency": "routine",
                "description": "Inflamación de la laringe",
                "recommendations": ["Reposo vocal", "Hidratación", "Humidificación", "Antiinflamatorios"],
                "red_flags": ["estridor", "disfagia", "fiebre alta"],
                "specialist": "otorrinolaringólogo",
                "duration": "1-2 semanas"
            },
            
            # HEMATOLÓGICO
            "anemia": {
                "symptoms": ["fatiga", "palidez", "disnea", "palpitaciones", "debilidad"],
                "urgency": "routine",
                "description": "Disminución de hemoglobina",
                "recommendations": ["Suplementos hierro", "Transfusión si severa", "Tratar causa"],
                "red_flags": ["anemia severa", "sangrado activo", "insuficiencia cardíaca"],
                "specialist": "hematólogo",
                "duration": "variable"
            },
            "leucemia": {
                "symptoms": ["fatiga", "fiebre", "infecciones", "sangrado", "pérdida peso"],
                "urgency": "emergency",
                "description": "Cáncer de células sanguíneas",
                "recommendations": ["Quimioterapia", "Trasplante médula ósea", "Soporte transfusional"],
                "red_flags": ["leucostasis", "síndrome lisis tumoral", "infecciones severas"],
                "specialist": "hematólogo",
                "duration": "meses a años"
            },
            "trombocitopenia": {
                "symptoms": ["petequias", "equimosis", "sangrado mucosas", "menorragia"],
                "urgency": "urgent",
                "description": "Disminución de plaquetas",
                "recommendations": ["Corticoides", "Inmunoglobulinas", "Transfusión plaquetas"],
                "red_flags": ["hemorragia intracraneal", "sangrado masivo", "cuenta <10.000"],
                "specialist": "hematólogo",
                "duration": "variable"
            },
            "linfoma": {
                "symptoms": ["adenopatías", "fiebre", "sudores nocturnos", "pérdida peso", "fatiga"],
                "urgency": "urgent",
                "description": "Cáncer del sistema linfático",
                "recommendations": ["Quimioterapia", "Radioterapia", "Inmunoterapia"],
                "red_flags": ["síndrome vena cava", "compresión medular", "síndrome lisis"],
                "specialist": "hematólogo",
                "duration": "meses a años"
            },
            
            # PSIQUIÁTRICO
            "depresion": {
                "symptoms": ["tristeza", "anhedonia", "fatiga", "alteraciones sueño", "sentimientos culpa"],
                "urgency": "routine",
                "description": "Trastorno del estado de ánimo",
                "recommendations": ["Antidepresivos", "Psicoterapia", "Cambios estilo vida"],
                "red_flags": ["ideación suicida", "síntomas psicóticos", "catatonia"],
                "specialist": "psiquiatra",
                "duration": "meses a años"
            },
            "ansiedad": {
                "symptoms": ["preocupación excesiva", "tensión", "palpitaciones", "sudoración", "temblor"],
                "urgency": "routine",
                "description": "Trastorno de ansiedad",
                "recommendations": ["Ansiolíticos", "Antidepresivos", "Terapia cognitivo-conductual"],
                "red_flags": ["ataques pánico", "agorafobia", "deterioro funcional"],
                "specialist": "psiquiatra",
                "duration": "crónica"
            },
            "trastorno_bipolar": {
                "symptoms": ["episodios manía", "episodios depresión", "cambios humor", "impulsividad"],
                "urgency": "urgent",
                "description": "Trastorno del estado de ánimo",
                "recommendations": ["Estabilizadores ánimo", "Antipsicóticos", "Psicoterapia"],
                "red_flags": ["episodio maníaco severo", "psicosis", "riesgo suicida"],
                "specialist": "psiquiatra",
                "duration": "crónica"
            },
            "esquizofrenia": {
                "symptoms": ["alucinaciones", "delirios", "desorganización", "síntomas negativos"],
                "urgency": "urgent",
                "description": "Trastorno psicótico crónico",
                "recommendations": ["Antipsicóticos", "Rehabilitación", "Soporte psicosocial"],
                "red_flags": ["agitación severa", "comportamiento violento", "catatonia"],
                "specialist": "psiquiatra",
                "duration": "crónica"
            },
            
            # INFECCIOSO
            "mononucleosis": {
                "symptoms": ["fiebre", "dolor garganta", "adenopatías", "fatiga", "esplenomegalia"],
                "urgency": "routine",
                "description": "Infección por virus Epstein-Barr",
                "recommendations": ["Reposo", "Analgésicos", "Hidratación", "Evitar deportes contacto"],
                "red_flags": ["ruptura esplénica", "obstrucción respiratoria", "hepatitis"],
                "specialist": None,
                "duration": "2-4 semanas"
            },
            "varicela": {
                "symptoms": ["erupción vesicular", "fiebre", "prurito", "malestar general"],
                "urgency": "routine",
                "description": "Infección por virus varicela-zóster",
                "recommendations": ["Antihistamínicos", "Antivirales si adulto", "Aislamiento"],
                "red_flags": ["neumonía", "encefalitis", "infección bacteriana secundaria"],
                "specialist": None,
                "duration": "1-2 semanas"
            },
            "hepatitis_viral": {
                "symptoms": ["ictericia", "fatiga", "náuseas", "dolor abdominal", "orina oscura"],
                "urgency": "urgent",
                "description": "Inflamación viral del hígado",
                "recommendations": ["Reposo", "Dieta", "Evitar hepatotóxicos", "Seguimiento"],
                "red_flags": ["falla hepática", "encefalopatía", "coagulopatía"],
                "specialist": "gastroenterólogo",
                "duration": "semanas a meses"
            },
            "covid19": {
                "symptoms": ["fiebre", "tos", "disnea", "anosmia", "fatiga"],
                "urgency": "routine",
                "description": "Infección por SARS-CoV-2",
                "recommendations": ["Aislamiento", "Sintomáticos", "Antivirales si indicado"],
                "red_flags": ["neumonía", "insuficiencia respiratoria", "tromboembolismo"],
                "specialist": None,
                "duration": "1-2 semanas"
            },
            
            # EMERGENCIAS
            "shock_anafilactico": {
                "symptoms": ["urticaria generalizada", "disnea", "hipotensión", "angioedema", "pérdida conciencia"],
                "urgency": "emergency",
                "description": "Reacción alérgica severa",
                "recommendations": ["Epinefrina", "Corticoides", "Antihistamínicos", "Soporte vital"],
                "red_flags": ["paro cardiorrespiratorio", "broncoespasmo severo", "colapso"],
                "specialist": "emergenciólogo",
                "duration": "emergencia"
            },
            "abdomen_agudo": {
                "symptoms": ["dolor abdominal severo", "rigidez", "náuseas", "vómitos", "fiebre"],
                "urgency": "emergency",
                "description": "Síndrome de emergencia abdominal",
                "recommendations": ["Evaluación quirúrgica", "Analgésicos", "Hidratación IV"],
                "red_flags": ["peritonitis", "shock", "distensión abdominal"],
                "specialist": "cirujano",
                "duration": "emergencia"
            },
            "convulsiones": {
                "symptoms": ["movimientos involuntarios", "pérdida conciencia", "incontinencia", "confusión post-ictal"],
                "urgency": "emergency",
                "description": "Crisis convulsiva",
                "recommendations": ["Protección vía aérea", "Benzodiacepinas", "Anticonvulsivantes"],
                "red_flags": ["status epilepticus", "traumatismo", "fiebre alta"],
                "specialist": "neurólogo",
                "duration": "emergencia"
            }
        }
        
        # Síntomas de emergencia absoluta
        self.emergency_symptoms = {
            "dolor_toracico_severo", "dolor_toracico_opresivo", "dolor_brazo_izquierdo",
            "dolor_mandibula", "sudoracion_profusa", "nauseas_con_dolor_toracico",
            "palpitaciones_severas", "taquicardia_extrema", "bradicardia_severa",
            "presion_arterial_muy_alta", "presion_arterial_muy_baja", "shock_cardiogenico",
            "edema_pulmonar_agudo", "cianosis_central", "dolor_toracico_punzante",
            "dificultad_respiratoria_severa", "disnea_extrema", "estridor_respiratorio",
            "cianosis_labios", "cianosis_unas", "respiracion_superficial",
            "apnea", "taquipnea_severa", "bradiapnea", "tos_con_sangre",
            "hemoptisis_abundante", "obstruccion_via_aerea", "respiracion_paradojica",
            "uso_musculos_accesorios", "tiraje_intercostal", "asfixia",
            "perdida_conciencia", "convulsiones", "estado_epileptico", "coma",
            "confusion_severa", "desorientacion_completa", "perdida_vision_subita",
            "vision_doble_subita", "debilidad_facial_subita", "paralisis_facial",
            "dificultad_hablar_subita", "afasia_subita", "paralisis_miembros",
            "hemiparesia_subita", "hemiplejia", "parestesias_severas",
            "cefalea_thunderclap", "cefalea_peor_vida", "rigidez_nuca",
            "fotofobia_severa", "perdida_equilibrio_subita", "vertigo_severo",
            "diplopia", "ptosis_subita", "pupilas_desiguales", "nistagmo",
            "ataxia_severa", "disartria_severa", "perdida_memoria_subita",
            "dolor_abdominal_severo", "vomito_sangre", "hematemesis", "melena",
            "hematoquecia", "sangrado_rectal_abundante", "vomito_proyectil",
            "vomito_bilioso", "distension_abdominal_severa", "abdomen_rigido",
            "defensa_abdominal", "rebote_abdominal", "murphy_positivo",
            "rovsing_positivo", "mcburney_dolor", "diarrea_sanguinolenta",
            "deshidratacion_severa", "ictericia_subita", "coluria",
            "acolia", "ascitis_severa",
            "sangrado_abundante", "hemorragia_arterial", "hemorragia_venosa",
            "shock_hipovolemico", "palidez_extrema", "llenado_capilar_lento",
            "pulso_debil", "hipotension_severa", "trauma_craneal",
            "fractura_expuesta", "deformidad_osea", "hematoma_grande",
            "equimosis_extensas", "penetracion_torax", "penetracion_abdomen",
            "herida_cuello", "amputacion_traumatica",
            "hipoglucemia_severa", "hiperglucemia_extrema", "cetoacidosis",
            "coma_diabetico", "deshidratacion_extrema", "hiponatremia_severa",
            "hipernatremia_severa", "hipopotasemia_severa", "hiperpotasemia_severa",
            "acidosis_metabolica", "alcalosis_metabolica", "hipocalcemia_severa",
            "hipercalcemia_severa", "uremia", "insuficiencia_renal_aguda"
            "fiebre_muy_alta", "hipertermia", "hipotermia_severa", "sepsis",
            "shock_septico", "meningitis_signos", "encefalitis_signos",
            "petequias_generalizadas", "purpura_fulminans", "celulitis_necrotizante",
            "fascitis_necrotizante", "gangrena", "absceso_cerebral_signos",
            "intoxicacion_severa", "sobredosis", "miosis_extrema", "midriasis_extrema",
            "convulsiones_toxicas", "coma_toxico", "depresion_respiratoria_toxica",
            "hipertermia_toxica", "rabdomiolisis", "sindrome_serotoninergico",
            "sindrome_anticolinergico", "sindrome_colinergico",
            "ideacion_suicida_activa", "intento_suicidio", "agitacion_psicomotriz",
            "agresividad_extrema", "psicosis_aguda", "episodio_maniaco_severo",
            "catatonia", "delirium_tremens", "alucinaciones_severas",
            "paranoia_extrema", "desorganizacion_severa",
            "perdida_vision_subita", "dolor_ocular_severo", "vision_halos",
            "glaucoma_agudo_signos", "desprendimiento_retina_signos",
            "cuerpo_extrano_ocular", "quemadura_ocular", "trauma_ocular",
            "obstruccion_via_aerea_superior", "estridor_inspiratorio",
            "disfagia_severa", "odinofagia_severa", "trismus", "angioedema",
            "epistaxis_severa", "cuerpo_extrano_via_aerea", "trauma_facial_severo",
            "anuria", "hematuria_severa", "dolor_lumbar_colico", "retencion_urinaria",
            "priapismo", "torsion_testicular_signos", "trauma_genital",
            "sangrado_vaginal_abundante", "dolor_pelvico_severo", "embarazo_ectopico_signos",
            "preeclampsia_signos", "eclampsia", "desprendimiento_placenta_signos",
            "parto_prematuro", "prolapso_cordon", "distocia_hombros",
            "llanto_inconsolable", "letargia_infantil", "fontanela_abombada",
            "fontanela_hundida", "cianosis_peribucal", "tiraje_subcostal",
            "estridor_pediatrico", "apnea_neonatal", "convulsion_febril_compleja",
            "deshidratacion_pediatrica_severa", "invaginacion_intestinal_signos",
            "caida_ancianos", "confusion_aguda_anciano", "incontinencia_subita",
            "perdida_funcional_subita", "sindrome_confusional_agudo",
            "hipotermia_accidental", "ulceras_presion_infectadas",
            "quemaduras_extensas", "quemaduras_segundo_grado", "quemaduras_tercer_grado",
            "sindrome_stevens_johnson", "necrolisis_epidermica_toxica",
            "angioedema_hereditario", "urticaria_generalizada", "anafilaxia_cutanea",
            "anafilaxia", "shock_anafilactico", "broncoespasmo_severo",
            "angioedema_laringeo", "urticaria_gigante", "hipotension_anafilactica",
            "edema_glotis", "prurito_generalizado_severo"
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
