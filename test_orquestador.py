#!/usr/bin/env python3
"""
Script de prueba para el orquestador de agentes médicos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from agents.orquestador import Orquestador
from agents.utils.funcionalidades import FuncionalidadMedica
from agents.analizarImagenes import AgenteAnalisisImagenes
from agents.busqueda import AgenteBusquedaCentros
from agents.diagnostico import AgenteDiagnostico
from agents.interpretacionExamenes import AgenteInterpretacionExamenes
from agents.explicacion import AgenteExplicacionMedica
from agents.contactoMedico import AgenteContactoMedico

def main():
    """Función principal para probar el orquestador"""
    
    # Cargar variables de entorno
    load_dotenv()
    
    print("🏥 Iniciando Sistema de Asistente Médico Inteligente")
    print("=" * 50)
    
    # Configuración del orquestador
    config = {
        "nombre": "Sistema Médico Inteligente",
        "version": "1.0",
        "modo": "desarrollo"
    }
    
    model_config = {
        "model_path": os.getenv("MODEL_PATH"),
        "n_threads": int(os.getenv("LLAMA_N_THREADS", os.cpu_count() or 8)),
        "n_batch": int(os.getenv("LLAMA_N_BATCH", 256)),
        "n_ctx": int(os.getenv("LLAMA_N_CTX", 2048)),
    }
    
    # Crear instancia del orquestador
    print("📋 Inicializando orquestador...")
    orquestador = Orquestador(config, model_config)
    
    # Crear e instanciar todos los agentes
    print("🤖 Creando agentes especializados...")
    
    agentes = {
        FuncionalidadMedica.DIAGNOSTICO: AgenteDiagnostico(),
        FuncionalidadMedica.ANALISIS_IMAGENES: AgenteAnalisisImagenes(),
        FuncionalidadMedica.INTERPRETACION_EXAMENES: AgenteInterpretacionExamenes(),
        FuncionalidadMedica.EXPLICACION_MEDICA: AgenteExplicacionMedica(),
        FuncionalidadMedica.BUSCADOR_CENTROS: AgenteBusquedaCentros(),
        FuncionalidadMedica.CONTACTO_MEDICO: AgenteContactoMedico(),
    }
    
    # Registrar todos los agentes en el orquestador
    for funcionalidad, agente in agentes.items():
        print(f"  ✅ Registrando {funcionalidad.value}")
        orquestador.registrar_agente(funcionalidad, agente)
    
    print("\n🎯 Sistema listo para recibir consultas")
    print("=" * 50)
    
    # Bucle principal de interacción
    session_id = None
    while True:
        # Obtener mensaje del usuario
        mensaje = input("\n👤 Usuario: ").strip()
        
        if mensaje.lower() in ['salir', 'exit', 'quit']:
            print("👋 ¡Hasta luego!")
            break
        
        if not mensaje:
            continue
        
        # Procesar mensaje con el orquestador
        print("\n🔄 Procesando mensaje...")
        resultado = orquestador.procesar_mensaje(session_id, mensaje)
        
        # Actualizar session_id si es la primera vez
        if not session_id:
            session_id = resultado["session_id"]
        
        # Mostrar resultado
        print(f"\n🤖 Respuesta ({resultado['funcionalidad']}):")
        print("-" * 30)
        
        if isinstance(resultado["respuesta"], dict):
            print(resultado["respuesta"].get("output", "Sin respuesta"))
        else:
            print(resultado["respuesta"])
        
        print("-" * 30)

if __name__ == "__main__":
    main() 