import os
from agents.interpretacionExamenes import AgenteInterpretacionExamenes

def main():
    print("\n=== Prueba de AgenteInterpretacionExamenes ===\n")
    agente = AgenteInterpretacionExamenes()
    session_id = "test"
    while True:
        pregunta = input("Ingrese los resultados del examen o escriba 'salir': ").strip()
        if pregunta.lower() in ("salir", "exit", "quit"):
            print("Adiós.")
            break
        respuesta = agente.preguntar(session_id, pregunta)
        if isinstance(respuesta, dict):
            print("\nRespuesta:")
            print(respuesta.get("output", "Sin respuesta"))
            if "metadata" in respuesta:
                print("Metadata:", respuesta["metadata"])
        else:
            print("\nRespuesta:")
            print(respuesta)
        print("-" * 40)

if __name__ == "__main__":
    main() 