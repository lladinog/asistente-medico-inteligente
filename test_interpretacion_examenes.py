"""
Script de pruebas CORREGIDO para verificar la integración del sistema de análisis de exámenes
con el orquestador.
"""

import sys
import os
import json
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.insert(0, root_dir)

from dotenv import load_dotenv
from agents.orquestador import Orquestador
from agents.interpretacionExamenes import AgenteInterpretacionExamenes
from agents.utils.funcionalidades import FuncionalidadMedica

# MOCK para agente de diagnóstico (para evitar errores de registro incompleto)
class MockAgenteDiagnostico:
    def __init__(self):
        pass
    
    def iniciar_interaccion(self, session_id: str, mensaje: str):
        return {"tipo": "diagnostico_mock"}
    
    def preguntar(self, session_id: str, pregunta: str, metadata=None):
        return {
            "output": f"Mock diagnóstico para: {pregunta[:50]}...",
            "metadata": {"tipo": "mock_response"}
        }

def setup_test_environment():
    """Configura el entorno de pruebas"""
    load_dotenv()
    
    # Configuración del sistema
    config = {
        "sistema": "Test Sistema Médico",
        "version": "1.0-test"
    }
    
    # Configuración del modelo
    model_config = {
        "model_path": os.getenv("MODEL_PATH"),
        "n_threads": int(os.getenv("LLAMA_N_THREADS", os.cpu_count() or 8)),
        "n_batch": int(os.getenv("LLAMA_N_BATCH", 256)),
        "n_ctx": int(os.getenv("LLAMA_N_CTX", 5000)),
        "temperature": 0.2,
        "max_tokens": 1024,
        "verbose": False 
    }
    
    return config, model_config

def crear_pdf_ejemplo():
    """Crea un archivo PDF de ejemplo para pruebas si no existe"""
    ejemplo_path = Path("agents/examen.pdf")
    
    if not ejemplo_path.exists():
        print("⚠️  No se encontró archivo PDF de prueba.")
        print(f"📝 Necesitas colocar un archivo PDF de examen en: {ejemplo_path.absolute()}")
        print("💡 O puedes cambiar la ruta en el script a un PDF existente.")
        return None
    
    return str(ejemplo_path)

def test_inicializacion():
    """Prueba 1: Verificar inicialización del sistema"""
    print("🧪 PRUEBA 1: Inicialización del Sistema")
    print("=" * 50)
    
    try:
        config, model_config = setup_test_environment()
        
        # Crear callback mock para el frontend
        def mock_frontend_callback(funcionalidad):
            print(f"[FRONTEND MOCK] Cambiando a: {funcionalidad}")
        
        # Crear orquestador con callback
        orquestador = Orquestador(config, model_config, frontend_callback=mock_frontend_callback)
        print("✅ Orquestador creado exitosamente")
        
        # Crear agente de interpretación de exámenes
        agente_examenes = AgenteInterpretacionExamenes()
        print("✅ Agente de interpretación creado exitosamente")
        
        # Crear agente mock de diagnóstico
        agente_diagnostico = MockAgenteDiagnostico()
        print("✅ Agente de diagnóstico mock creado")
        
        # Registrar ambos agentes en orquestador
        orquestador.registrar_agente(FuncionalidadMedica.INTERPRETACION_EXAMENES, agente_examenes)
        orquestador.registrar_agente(FuncionalidadMedica.DIAGNOSTICO, agente_diagnostico)
        print("✅ Agentes registrados en orquestador")
        
        # Verificar que el agente PDF interno esté disponible
        if hasattr(agente_examenes, 'pdf_agent'):
            print("✅ Agente PDF interno disponible")
            info = agente_examenes.pdf_agent.get_system_info()
            print(f"📊 Capacidades del agente PDF: {len(info['capabilities'])} funciones")
        else:
            print("❌ Agente PDF interno no disponible")
            return False
        
        # Verificar agentes registrados
        print(f"📋 Agentes registrados: {list(orquestador.agentes.keys())}")
        
        return orquestador, agente_examenes
        
    except Exception as e:
        print(f"❌ Error en inicialización: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_clasificacion_directa(orquestador):
    """Prueba 2A: Verificar clasificación directa sin usar el clasificador automático"""
    print("\n🧪 PRUEBA 2A: Clasificación Directa (Bypass)")
    print("=" * 50)
    
    # Prueba directa del agente de exámenes
    try:
        agente_examenes = orquestador.agentes.get('interpretacion_examenes')
        if agente_examenes:
            respuesta = agente_examenes.preguntar(
                session_id="test_directo",
                pregunta="Quiero analizar mi examen de sangre"
            )
            print("✅ Agente de exámenes responde directamente")
            print(f"📝 Respuesta: {respuesta.get('output', '')[:100]}...")
        else:
            print("❌ No se encontró agente de exámenes")
            
    except Exception as e:
        print(f"❌ Error en prueba directa: {str(e)}")
    
    return True

def test_clasificacion_forzada(orquestador):
    """Prueba 2B: Forzar la clasificación correcta"""
    print("\n🧪 PRUEBA 2B: Clasificación Forzada")
    print("=" * 50)
    
    # Modificar temporalmente el método de clasificación
    def _determinar_funcionalidad_forzada(mensaje: str) -> str:
        """Versión simplificada para pruebas"""
        mensaje_lower = mensaje.lower()
        
        palabras_examenes = ['examen', 'analisis', 'laboratorio', 'pdf', 'resultado', 'hemograma', 'sangre']
        
        if any(palabra in mensaje_lower for palabra in palabras_examenes):
            return 'interpretacion_examenes'
        else:
            return 'diagnostico'
    
    # Reemplazar el método temporalmente
    metodo_original = orquestador._determinar_funcionalidad
    orquestador._determinar_funcionalidad = _determinar_funcionalidad_forzada
    
    mensajes_test = [
        "Quiero analizar mi examen de sangre",
        "Tengo un PDF con los resultados de mi hemograma", 
        "¿Puedes interpretar estos valores de laboratorio?",
        "Me duele la cabeza, ¿qué podría ser?",
        "Analiza mi radiografía"
    ]
    
    for mensaje in mensajes_test:
        try:
            resultado = orquestador.procesar_mensaje("test_session", mensaje)
            funcionalidad = resultado.get("funcionalidad", "desconocida")
            print(f"📝 '{mensaje[:40]}...' → {funcionalidad}")
            
            # Verificar respuesta
            respuesta = resultado.get("respuesta", {})
            if isinstance(respuesta, dict) and respuesta.get("output"):
                print(f"   ✅ Respuesta obtenida: {respuesta['output'][:100]}...")
            else:
                print(f"   ⚠️  Respuesta inesperada: {type(respuesta)} - {respuesta}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Restaurar método original
    orquestador._determinar_funcionalidad = metodo_original
    return True

def test_procesamiento_archivo_directo(orquestador):
    """Prueba 3: Verificar procesamiento directo de archivos PDF"""
    print("\n🧪 PRUEBA 3: Procesamiento Directo de Archivos PDF")
    print("=" * 50)
    
    # Buscar archivo PDF de prueba
    pdf_path = crear_pdf_ejemplo()
    
    if not pdf_path:
        print("⏭️  Saltando prueba de PDF (no hay archivo disponible)")
        return True, None
    
    print(f"📄 Usando archivo: {pdf_path}")
    
    try:
        # Obtener agente directamente
        agente_examenes = orquestador.agentes.get('interpretacion_examenes')
        if not agente_examenes:
            print("❌ No se encontró agente de exámenes")
            return False, None
        
        # Probar procesamiento directo del PDF
        resultado = agente_examenes.procesar_archivo_pdf(
            session_id="test_pdf_directo",
            pdf_path=pdf_path,
            patient_context="Paciente de prueba, 30 años, sin antecedentes conocidos",
            patient_level="intermedio"
        )
        
        print(f"🔄 Procesamiento directo completado")
        print(f"✅ Éxito: {resultado.get('metadata', {}).get('tipo', 'desconocido')}")
        
        # Mostrar parte de la respuesta
        output = resultado.get('output', '')
        if output:
            print(f"📝 Respuesta (primeros 200 chars): {output[:200]}...")
            return True, "test_pdf_directo"
        else:
            print(f"⚠️  No se obtuvo output. Resultado completo: {resultado}")
            return False, None
        
    except Exception as e:
        print(f"❌ Error procesando PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None

def test_procesamiento_archivo_orquestador(orquestador):
    """Prueba 3B: Verificar procesamiento a través del orquestador"""
    print("\n🧪 PRUEBA 3B: Procesamiento via Orquestador")
    print("=" * 50)
    
    # Buscar archivo PDF de prueba
    pdf_path = crear_pdf_ejemplo()
    
    if not pdf_path:
        print("⏭️  Saltando prueba de PDF (no hay archivo disponible)")
        return True, None
    
    print(f"📄 Usando archivo: {pdf_path}")
    
    try:
        # Procesar archivo a través del orquestador
        resultado = orquestador.procesar_archivo_medico(
            session_id="test_pdf_orq",
            archivo_path=pdf_path,
            patient_context="Paciente de prueba, 30 años, sin antecedentes conocidos",
            patient_level="intermedio"
        )
        
        print(f"🔄 Procesamiento via orquestador completado")
        print(f"📊 Funcionalidad detectada: {resultado.get('funcionalidad')}")
        print(f"✅ Éxito: {resultado.get('respuesta', {}).get('metadata', {}).get('tipo', 'desconocido')}")
        
        # Mostrar parte de la respuesta
        output = resultado.get('respuesta', {}).get('output', '')
        if output:
            print(f"📝 Respuesta (primeros 200 chars): {output[:200]}...")
        
        return True, resultado.get('session_id')
        
    except Exception as e:
        print(f"❌ Error procesando PDF via orquestador: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None

def test_conversacion_contextual(orquestador, session_id):
    """Prueba 4: Verificar conversación contextual"""
    print("\n🧪 PRUEBA 4: Conversación Contextual")
    print("=" * 50)
    
    if not session_id:
        print("⏭️  Saltando prueba contextual (no hay sesión previa)")
        return True
    
    preguntas_test = [
        "¿Qué significan estos resultados?",
        "¿Los valores están dentro de lo normal?",
    ]
    
    for pregunta in preguntas_test:
        try:
            # Usar el método directo del agente
            agente_examenes = orquestador.agentes.get('interpretacion_examenes')
            if agente_examenes:
                resultado = agente_examenes.preguntar(
                    session_id=session_id,
                    pregunta=pregunta
                )
                
                print(f"❓ Pregunta: {pregunta}")
                output = resultado.get('output', '') if isinstance(resultado, dict) else str(resultado)
                if output:
                    print(f"💬 Respuesta (primeros 150 chars): {output[:150]}...")
                
                if isinstance(resultado, dict):
                    metadata = resultado.get('metadata', {})
                    if metadata.get('uso_contexto_previo'):
                        print("   ✅ Usó contexto previo correctamente")
                    else:
                        print("   ⚠️  No detectó contexto previo")
                
                print()
            else:
                print(f"❌ No se encontró agente de exámenes")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    return True

def test_debug_clasificador(orquestador):
    """Prueba DEBUG: Verificar qué está pasando con el clasificador"""
    print("\n🧪 PRUEBA DEBUG: Análisis del Clasificador")
    print("=" * 50)
    
    mensaje_test = "Quiero analizar mi examen de sangre"
    
    try:
        print(f"📝 Mensaje de prueba: '{mensaje_test}'")
        
        # Probar clasificador directamente
        respuesta_clasificador = orquestador.agente_clasificador.preguntar(
            session_id="debug_clasificador",
            pregunta=f"Clasifica este mensaje en una de estas categorías: {', '.join([f.value for f in FuncionalidadMedica])}. Solo responde con el nombre de la categoría. Mensaje: {mensaje_test}"
        )
        
        print(f"🔍 Respuesta del clasificador: '{respuesta_clasificador}'")
        print(f"🔍 Tipo de respuesta: {type(respuesta_clasificador)}")
        
        # Analizar la respuesta
        if isinstance(respuesta_clasificador, dict):
            funcionalidad = respuesta_clasificador.get('output', '').strip().lower()
        else:
            funcionalidad = str(respuesta_clasificador).strip().lower()
        
        print(f"🔍 Funcionalidad extraída: '{funcionalidad}'")
        
        # Verificar si está en agentes registrados
        agentes_disponibles = list(orquestador.agentes.keys())
        print(f"🔍 Agentes disponibles: {agentes_disponibles}")
        
        if funcionalidad in orquestador.agentes:
            print(f"✅ Funcionalidad '{funcionalidad}' encontrada en agentes")
        else:
            print(f"❌ Funcionalidad '{funcionalidad}' NO encontrada en agentes")
            print(f"💡 Usando diagnóstico por defecto")
        
    except Exception as e:
        print(f"❌ Error en debug del clasificador: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return True

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS CORREGIDAS DEL SISTEMA DE ANÁLISIS DE EXÁMENES")
    print("=" * 70)
    
    # Prueba 1: Inicialización
    resultado_init = test_inicializacion()
    if not resultado_init:
        print("❌ Falló la inicialización. Deteniendo pruebas.")
        return
    
    orquestador, agente_examenes = resultado_init
    
    # Prueba DEBUG: Analizar el clasificador
    test_debug_clasificador(orquestador)
    
    # Prueba 2A: Clasificación directa
    test_clasificacion_directa(orquestador)
    
    # Prueba 2B: Clasificación forzada
    test_clasificacion_forzada(orquestador)
    
    # Prueba 3A: Procesamiento directo
    resultado_pdf_directo, session_id_directo = test_procesamiento_archivo_directo(orquestador)
    
    # Prueba 3B: Procesamiento via orquestador
    resultado_pdf_orq, session_id_orq = test_procesamiento_archivo_orquestador(orquestador)
    
    # Prueba 4: Conversación contextual
    session_id_para_contexto = session_id_directo or session_id_orq
    if session_id_para_contexto:
        test_conversacion_contextual(orquestador, session_id_para_contexto)
    
    print("\n🎉 PRUEBAS COMPLETADAS")
    print("=" * 70)

if __name__ == "__main__":
    main()