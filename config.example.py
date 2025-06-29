# Configuración de ejemplo para el Asistente Médico Inteligente
# Copia este archivo como config.py y ajusta los valores según tus necesidades

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    """Configuración de la aplicación"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'tu_clave_api_de_openai_aqui')
    
    # Configuración de la aplicación
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', 8050))
    
    # Configuración de modelos
    MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-4')
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.1))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 2000))
    
    # Configuración de base de datos (opcional)
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///asistente_medico.db')
    
    # Configuración de logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/asistente_medico.log')
    
    # Configuración de seguridad
    SECRET_KEY = os.getenv('SECRET_KEY', 'tu_clave_secreta_aqui')
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    
    # Configuración de modelos de visión
    VISION_MODEL = os.getenv('VISION_MODEL', 'microsoft/resnet-50')
    VISION_DEVICE = os.getenv('VISION_DEVICE', 'cpu')
    
    # Configuración de cache
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))

# Instancia de configuración
config = Config() 