"""
Agente de análisis de PDFs de exámenes médicos
Integra análisis de documentos PDF con el sistema de diagnóstico médico
"""

import sys
import os
import json
import uuid
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

import fitz  
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain_core.runnables import RunnableWithMessageHistory

# Agregar el directorio raíz al path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.insert(0, root_dir)

from agents.utils.conversation import Conversation

class MedicalPDFAnalysisAgent:
    """Agente especializado en análisis de PDFs de exámenes médicos"""
    
    def __init__(self, model_config: Dict[str, Any]):
        """
        Inicializa el agente de análisis de PDFs
        
        Args:
            model_config (dict): Configuración del modelo LLaMA
        """
        self.model_config = model_config
        self.analysis_history = {}
        
        # Inicializar modelo LLaMA específico para análisis de exámenes
        self._setup_llm()
        self._setup_prompts()
        self._setup_chains()
        
        # Configurar directorio de trabajo
        self.work_dir = Path("pdf_analysis")
        self.work_dir.mkdir(exist_ok=True)
        
        print("✅ Agente de análisis de PDFs médicos inicializado")
    
    def _setup_llm(self):
        """Configura el modelo LLaMA para análisis médico"""
        self.llm = LlamaCpp(
            model_path= os.getenv("MODEL_PATH", r"C:\Users\HP\Downloads\llama-2-7b-chat.Q4_K_M.gguf"),
            n_ctx=self.model_config.get("n_ctx", 4096), 
            n_threads=self.model_config.get("n_threads", 8),
            n_batch=self.model_config.get("n_batch", 1024),
            temperature=0.2, 
            max_tokens=1024, 
            top_p=0.9,
            repeat_penalty=1.1,
            stop=["Paciente:", "PACIENTE:", "Usuario:", "USUARIO:", "Human:", "HUMAN:"],
            verbose=False,
        )
    
    def _setup_prompts(self):
        """Configura los prompts especializados para análisis de exámenes"""
        
        # Prompt para clasificar tipo de examen
        self.exam_classifier_prompt = PromptTemplate(
            input_variables=["exam_text"],
            template="""
Eres un médico especialista en interpretación de exámenes de laboratorio e imágenes médicas.

Analiza el siguiente texto extraído de un examen médico y clasifica qué tipo de examen es:

TEXTO DEL EXAMEN:
{exam_text}

Debes responder ÚNICAMENTE con la clasificación en el siguiente formato JSON:
{{
    "tipo_examen": "tipo específico del examen (ej: hemograma, química sanguínea, radiografía, etc.)",
    "categoria": "categoría general (laboratorio/imagen/funcional/biopsia/etc.)",
    "especialidad": "especialidad médica relacionada",
    "confianza": "nivel de confianza de 0.0 a 1.0"
}}

Clasificación:"""
        )
        
        # Prompt para análisis detallado del examen
        self.exam_analysis_prompt = PromptTemplate(
            input_variables=["exam_text", "exam_type", "patient_context"],
            template="""
Eres un médico especialista experto en interpretación de exámenes médicos.

INFORMACIÓN DEL EXAMEN:
Tipo: {exam_type}
Contexto del paciente: {patient_context}

RESULTADOS DEL EXAMEN:
{exam_text}

Realiza un análisis médico completo y detallado:

1. VALORES ANALIZADOS:
   - Identifica todos los parámetros medidos
   - Clasifica cada valor como normal, alterado (alto/bajo), o crítico
   - Explica el significado clínico de cada alteración

2. INTERPRETACIÓN CLÍNICA:
   - ¿Qué indican estos resultados sobre la salud del paciente?
   - ¿Hay patrones o correlaciones entre los valores?
   - ¿Qué condiciones médicas podrían explicar estos hallazgos?

3. NIVEL DE URGENCIA:
   - Evalúa si hay valores críticos que requieren atención inmediata
   - Clasifica como: NORMAL / SEGUIMIENTO / URGENTE / CRÍTICO

4. RECOMENDACIONES:
   - ¿Qué acciones médicas se recomiendan?
   - ¿Se necesitan exámenes adicionales?
   - ¿Cuándo debe repetirse este examen?

Proporciona una explicación clara y comprensible, usando términos médicos apropiados pero explicando su significado.

ANÁLISIS MÉDICO:"""
        )
        
        # Prompt para explicación simple para pacientes
        self.patient_explanation_prompt = PromptTemplate(
            input_variables=["medical_analysis", "patient_level"],
            template="""
Eres un médico que debe explicar resultados de exámenes a un paciente de manera clara y comprensible.

ANÁLISIS MÉDICO TÉCNICO:
{medical_analysis}

NIVEL DEL PACIENTE: {patient_level}

Explica estos resultados de manera que el paciente pueda entender:

1. RESUMEN GENERAL:
   - ¿Los resultados son normales o hay algo que requiere atención?
   - Usa un lenguaje simple y tranquilizador cuando sea apropiado

2. HALLAZGOS PRINCIPALES:
   - Explica los hallazgos más importantes en términos simples
   - Evita jerga médica excesiva
   - Si hay alteraciones, explica qué significan y por qué pueden ocurrir

3. QUÉ SIGUE:
   - ¿Qué debe hacer el paciente con estos resultados?
   - ¿Es necesario consultar con un médico inmediatamente?
   - ¿Hay cambios en el estilo de vida que podrían ayudar?

4. TRANQUILIDAD O PRECAUCIÓN:
   - Si los resultados son normales, tranquiliza al paciente
   - Si hay problemas, explica sin alarmar innecesariamente
   - Enfatiza la importancia del seguimiento médico apropiado

EXPLICACIÓN PARA EL PACIENTE:"""
        )
    
    def _setup_chains(self):
        """Configura las cadenas de procesamiento"""
        self.classifier_chain = self.exam_classifier_prompt | self.llm
        self.analysis_chain = self.exam_analysis_prompt | self.llm
        self.explanation_chain = self.patient_explanation_prompt | self.llm
        
        self.history_factory = lambda session_id: Conversation(
            file_path=f"pdf_analysis/session_{session_id}.json",
            max_tokens=self.model_config.get("n_ctx", 4096) - 1024,
            buffer_extra=1024
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> Tuple[str, Dict[str, Any]]:
        """
        Extrae texto de un PDF médico
        
        Args:
            pdf_path (str): Ruta al archivo PDF
            
        Returns:
            tuple: (texto_extraído, metadatos)
        """
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            metadata = {
                "num_pages": len(doc),
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "creation_date": doc.metadata.get("creationDate", ""),
                "pages_info": []
            }
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                full_text += f"\n--- PÁGINA {page_num + 1} ---\n{text}\n"
                
                metadata["pages_info"].append({
                    "page": page_num + 1,
                    "char_count": len(text),
                    "has_images": len(page.get_images()) > 0
                })
            
            doc.close()
            
            # Limpiar y estructurar el texto
            cleaned_text = self._clean_extracted_text(full_text)
            
            return cleaned_text, metadata
            
        except Exception as e:
            raise Exception(f"Error extrayendo texto del PDF: {str(e)}")
    
    def _clean_extracted_text(self, text: str) -> str:
        """Limpia y estructura el texto extraído"""
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        patterns = {
            'patient_info': r'(nombre|paciente|edad|sexo|fecha.*nacimiento)',
            'exam_date': r'(fecha.*examen|fecha.*muestra|fecha.*estudio)',
            'doctor_info': r'(médico.*solicita|doctor|dra?\.|solicitado.*por)',
            'results': r'(resultado|valor|referencia|normal|anormal)',
            'observations': r'(observacion|comentario|nota|interpretación)'
        }

        for section, pattern in patterns.items():
            text = re.sub(f'({pattern})', r'[SECCIÓN_\1]', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def classify_exam_type(self, exam_text: str) -> Dict[str, Any]:
        """
        Clasifica el tipo de examen médico
        
        Args:
            exam_text (str): Texto del examen
            
        Returns:
            dict: Clasificación del examen
        """
        try:
            # Truncar texto si es muy largo
            max_chars = 2000
            if len(exam_text) > max_chars:
                exam_text = exam_text[:max_chars] + "..."
            
            response = self.classifier_chain.invoke({"exam_text": exam_text})
            
            # Intentar parsear la respuesta como JSON
            try:
                classification = json.loads(response.strip())
                classification["success"] = True
                classification["timestamp"] = datetime.now().isoformat()
                return classification
            except json.JSONDecodeError:
                # Si no es JSON válido, extraer información manualmente
                return self._parse_classification_text(response)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tipo_examen": "desconocido",
                "categoria": "general",
                "especialidad": "medicina general",
                "confianza": 0.0,
                "timestamp": datetime.now().isoformat()
            }
    
    def _parse_classification_text(self, response_text: str) -> Dict[str, Any]:
        """Parsea la respuesta de clasificación cuando no es JSON"""
        classification = {
            "success": True,
            "tipo_examen": "examen médico",
            "categoria": "general",
            "especialidad": "medicina general",
            "confianza": 0.5,
            "timestamp": datetime.now().isoformat()
        }
        
        response_lower = response_text.lower()
        
        # Tipos de examen comunes
        exam_types = {
            "hemograma": ["hemograma", "hematología", "conteo sanguíneo"],
            "química sanguínea": ["química", "glucosa", "colesterol", "triglicéridos"],
            "orina": ["orina", "urinálisis", "examen de orina"],
            "radiografía": ["radiografía", "rayos x", "rx"],
            "ecografía": ["ecografía", "ultrasonido", "eco"],
            "tomografía": ["tomografía", "tac", "ct scan"],
            "resonancia": ["resonancia", "rmn", "mri"]
        }
        
        for exam_type, keywords in exam_types.items():
            if any(keyword in response_lower for keyword in keywords):
                classification["tipo_examen"] = exam_type
                classification["confianza"] = 0.8
                break
        
        return classification
    
    def analyze_exam(self, exam_text: str, exam_type: str, patient_context: str = "", session_id: str = None) -> Dict[str, Any]:
        """
        Realiza análisis médico completo del examen
        
        Args:
            exam_text (str): Texto del examen
            exam_type (str): Tipo de examen clasificado
            patient_context (str): Contexto del paciente
            session_id (str): ID de sesión para mantener contexto
            
        Returns:
            dict: Análisis médico completo
        """
        try:
            # Truncar texto si es muy largo
            max_chars = 3000
            if len(exam_text) > max_chars:
                exam_text = exam_text[:max_chars] + "..."
            
            analysis_response = self.analysis_chain.invoke({
                "exam_text": exam_text,
                "exam_type": exam_type,
                "patient_context": patient_context or "No se proporcionó contexto adicional"
            })
            
            cleaned_analysis = self._clean_response(analysis_response)
            
            urgency_level = self._extract_urgency_level(cleaned_analysis)
            
            result = {
                "success": True,
                "analysis": cleaned_analysis,
                "urgency_level": urgency_level,
                "exam_type": exam_type,
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id
            }
            
            if session_id:
                self._save_analysis_to_history(session_id, result)
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis": f"Error en el análisis: {str(e)}",
                "urgency_level": "DESCONOCIDO",
                "exam_type": exam_type,
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id
            }
    
    def explain_for_patient(self, medical_analysis: str, patient_level: str = "intermedio") -> str:
        """
        Genera explicación comprensible para el paciente
        
        Args:
            medical_analysis (str): Análisis médico técnico
            patient_level (str): Nivel de explicación (simple/intermedio/detallado)
            
        Returns:
            str: Explicación para el paciente
        """
        try:
            explanation = self.explanation_chain.invoke({
                "medical_analysis": medical_analysis,
                "patient_level": patient_level
            })
            
            return self._clean_response(explanation)
            
        except Exception as e:
            return f"Error generando explicación: {str(e)}"
    
    def process_pdf_exam(self, pdf_path: str, patient_context: str = "", patient_level: str = "intermedio", session_id: str = None) -> Dict[str, Any]:
        """
        Procesa un PDF de examen médico completo
        
        Args:
            pdf_path (str): Ruta al archivo PDF
            patient_context (str): Contexto del paciente
            patient_level (str): Nivel de explicación
            session_id (str): ID de sesión
            
        Returns:
            dict: Resultado completo del análisis
        """
        analysis_id = str(uuid.uuid4())
        
        try:
            # 1. Extraer texto del PDF
            print("📄 Extrayendo texto del PDF...")
            exam_text, metadata = self.extract_text_from_pdf(pdf_path)
            
            if not exam_text.strip():
                raise Exception("No se pudo extraer texto del PDF")
            
            # 2. Clasificar tipo de examen
            print("🔍 Clasificando tipo de examen...")
            classification = self.classify_exam_type(exam_text)
            
            # 3. Realizar análisis médico
            print("⚕️ Realizando análisis médico...")
            medical_analysis = self.analyze_exam(
                exam_text, 
                classification.get("tipo_examen", "examen médico"),
                patient_context,
                session_id
            )
            
            # 4. Generar explicación para paciente
            print("💬 Generando explicación para paciente...")
            patient_explanation = ""
            if medical_analysis.get("success"):
                patient_explanation = self.explain_for_patient(
                    medical_analysis["analysis"], 
                    patient_level
                )
            
            # 5. Compilar resultado final
            result = {
                "analysis_id": analysis_id,
                "success": True,
                "pdf_info": {
                    "filename": os.path.basename(pdf_path),
                    "metadata": metadata
                },
                "classification": classification,
                "medical_analysis": medical_analysis,
                "patient_explanation": patient_explanation,
                "processing_time": datetime.now().isoformat(),
                "session_id": session_id
            }
            
            # 6. Guardar resultado completo
            self._save_complete_analysis(analysis_id, result)
            
            print("✅ Análisis completado exitosamente")
            return result
            
        except Exception as e:
            error_result = {
                "analysis_id": analysis_id,
                "success": False,
                "error": str(e),
                "pdf_info": {"filename": os.path.basename(pdf_path)},
                "processing_time": datetime.now().isoformat(),
                "session_id": session_id
            }
            
            print(f"❌ Error en el análisis: {str(e)}")
            return error_result
    
    def _extract_urgency_level(self, analysis_text: str) -> str:
        """Extrae el nivel de urgencia del análisis"""
        analysis_lower = analysis_text.lower()
        
        if any(word in analysis_lower for word in ["crítico", "emergencia", "inmediato", "urgente"]):
            return "CRÍTICO"
        elif any(word in analysis_lower for word in ["urgente", "pronto", "seguimiento urgente"]):
            return "URGENTE"
        elif any(word in analysis_lower for word in ["seguimiento", "control", "repetir"]):
            return "SEGUIMIENTO"
        else:
            return "NORMAL"
    
    def _clean_response(self, response: str) -> str:
        """Limpia las respuestas del modelo"""
        response = re.sub(r'(Paciente:|PACIENTE:|Usuario:|USUARIO:).*', '', response)
        response = re.sub(r'\n\s*\n', '\n\n', response)
        response = response.strip()
        
        return response
    
    def _save_analysis_to_history(self, session_id: str, analysis: Dict[str, Any]):
        """Guarda análisis en el historial de la sesión"""
        if session_id not in self.analysis_history:
            self.analysis_history[session_id] = []
        
        self.analysis_history[session_id].append({
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        })
    
    def _save_complete_analysis(self, analysis_id: str, result: Dict[str, Any]):
        """Guarda el análisis completo en archivo"""
        analysis_file = self.work_dir / f"analysis_{analysis_id}.json"
        
        try:
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error guardando análisis: {str(e)}")
    
    def get_analysis_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Obtiene el historial de análisis de una sesión"""
        return self.analysis_history.get(session_id, [])
    
    def get_supported_formats(self) -> List[str]:
        """Obtiene los formatos de archivo soportados"""
        return [".pdf"]
    
    def get_system_info(self) -> Dict[str, Any]:
        """Obtiene información del sistema de análisis"""
        return {
            "system_name": "Agente de Análisis de PDFs Médicos",
            "version": "1.0",
            "supported_formats": self.get_supported_formats(),
            "capabilities": [
                "Extracción de texto de PDFs",
                "Clasificación automática de exámenes",
                "Análisis médico detallado",
                "Explicaciones comprensibles para pacientes",
                "Evaluación de urgencia médica",
                "Historial de análisis por sesión"
            ],
            "exam_types_supported": [
                "Análisis de laboratorio (hemograma, química sanguínea, etc.)",
                "Estudios de imagen (radiografías, ecografías, etc.)",
                "Estudios funcionales",
                "Biopsias y patología",
                "Cualquier examen médico en formato PDF"
            ],
            "timestamp": datetime.now().isoformat()
        }


def create_pdf_analysis_agent(model_config: Dict[str, Any]) -> MedicalPDFAnalysisAgent:
    """
    Crea una instancia del agente de análisis de PDFs
    
    Args:
        model_config (dict): Configuración del modelo LLaMA
        
    Returns:
        MedicalPDFAnalysisAgent: Instancia del agente
    """
    return MedicalPDFAnalysisAgent(model_config)


# Función de prueba
if __name__ == "__main__":
    # Configuración de prueba
    test_model_config = {
        "model_path": os.getenv("MODEL_PATH"),
        "n_threads": 8,
        "n_batch": 1024,
        "n_ctx": 4096,
        "temperature": 0.2,
        "max_tokens": 1024,
        "top_p": 0.9,
        "repeat_penalty": 1.1,
        "verbose": False
    }
    
    # Crear agente
    pdf_agent = create_pdf_analysis_agent(test_model_config)
    
    # Mostrar información del sistema
    print(json.dumps(pdf_agent.get_system_info(), indent=2, ensure_ascii=False))
    
    result = pdf_agent.process_pdf_exam(
        pdf_path="agents/examen.pdf",
        patient_context="Paciente femenino, 19 años, enfermedad no conocida",
        patient_level="intermedio",
       session_id="test_001"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))