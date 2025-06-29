# Configuración y constantes de la aplicación

# Datos mockeados para centros médicos
CENTROS_MEDICOS = {
    "Antioquia": [
        {"nombre": "Hospital San Rafael", "municipio": "Medellín", "direccion": "Calle 50 #30-20", "telefono": "604-555-0123", "distancia": "15 km", "especialidades": ["Medicina General", "Urgencias", "Pediatría"]},
        {"nombre": "Centro de Salud La Paz", "municipio": "Bello", "direccion": "Carrera 20 #45-30", "telefono": "604-555-0456", "distancia": "8 km", "especialidades": ["Medicina General", "Ginecología"]},
        {"nombre": "Puesto de Salud Rural", "municipio": "Barbosa", "direccion": "Vereda El Progreso", "telefono": "604-555-0789", "distancia": "5 km", "especialidades": ["Medicina General"]},
    ],
    "Cundinamarca": [
        {"nombre": "Hospital Central", "municipio": "Bogotá", "direccion": "Avenida 68 #40-50", "telefono": "601-555-0321", "distancia": "25 km", "especialidades": ["Medicina General", "Urgencias", "Cardiología"]},
        {"nombre": "Centro de Salud Suba", "municipio": "Bogotá", "direccion": "Calle 145 #91-20", "telefono": "601-555-0654", "distancia": "12 km", "especialidades": ["Medicina General", "Pediatría"]},
    ]
}

# Datos mockeados para médicos
MEDICOS_ASIGNADOS = [
    {"nombre": "Dr. Carlos Mendoza", "especialidad": "Medicina General", "centro": "Hospital San Rafael", "disponibilidad": "Lunes a Viernes 8:00-16:00"},
    {"nombre": "Dra. Ana María López", "especialidad": "Pediatría", "centro": "Centro de Salud La Paz", "disponibilidad": "Martes y Jueves 9:00-13:00"},
    {"nombre": "Dr. Roberto Silva", "especialidad": "Medicina Rural", "centro": "Puesto de Salud Rural", "disponibilidad": "Lunes, Miércoles y Viernes 7:00-15:00"},
]

# Estilos personalizados
COLORS = {
    'primary': '#0066CC',      
    'secondary': '#4A90E2',    
    'accent': '#FF6B6B',       
    'success': '#28A745',     
    'warning': '#FFC107',     
    'info': '#17A2B8',       
    'background': '#F8FBFF', 
    'text': '#2C3E50',
    'white': '#FFFFFF',
    'light_blue': '#E3F2FD',  
    'dark_blue': '#003D82'  
}

COORDENADAS_CENTROS = {
    "Antioquia": [
        {"nombre": "Hospital San Rafael", "lat": 6.2476, "lng": -75.5658, "municipio": "Medellín"},
        {"nombre": "Centro de Salud La Paz", "lat": 6.3369, "lng": -75.5542, "municipio": "Bello"},
        {"nombre": "Puesto de Salud Rural", "lat": 6.4395, "lng": -75.6207, "municipio": "Barbosa"},
    ],
    "Cundinamarca": [
        {"nombre": "Hospital Central", "lat": 4.6097, "lng": -74.0817, "municipio": "Bogotá"},
        {"nombre": "Centro de Salud Suba", "lat": 4.7570, "lng": -74.0814, "municipio": "Bogotá"},
    ]
} 