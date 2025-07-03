# Configuración de ejemplo para Health IA
# Copia este archivo como config.py y ajusta los valores según tus necesidades
import os

class Config:
    """Configuración principal de Health IA"""

    # -------------------------------
    # Configuración general de la app
    # -------------------------------
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', 8050))

    # -------------------------------
    # Configuración del modelo LLM
    # -------------------------------
    MODEL_PATH = os.getenv('MODEL_PATH')  # Ruta al archivo GGUF de llama.cpp
    LLAMA_N_THREADS = int(os.getenv('LLAMA_N_THREADS', 4))  # Se detecta automáticamente en setup
    LLAMA_N_BATCH = int(os.getenv('LLAMA_N_BATCH', 256))
    LLAMA_N_CTX = int(os.getenv('LLAMA_N_CTX', 2048))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.5))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 256))

    # -------------------------------
    # Configuración de seguridad
    # -------------------------------
    SECRET_KEY = os.getenv('SECRET_KEY', 'tu_clave_secreta_aqui')
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

    # -------------------------------
    # Configuración de logging
    # -------------------------------
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/asistente_medico.log')

    # -------------------------------
    # Configuración opcional de base de datos
    # -------------------------------
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///asistente_medico.db')

    # -------------------------------
    # Configuración de modelo de visión
    # -------------------------------
    VISION_MODEL = os.getenv('VISION_MODEL', 'microsoft/resnet-50')
    VISION_DEVICE = os.getenv('VISION_DEVICE', 'cpu')

    # -------------------------------
    # Configuración de cache
    # -------------------------------
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))


# Instancia global para importar en otros módulos
config = Config()
