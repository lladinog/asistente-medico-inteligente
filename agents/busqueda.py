import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import json
import requests
from typing import Optional, Dict, List, Tuple
from dotenv import load_dotenv
from dataclasses import dataclass
from math import radians, cos, sin, asin, sqrt

from agents.agente import Agente

@dataclass
class CentroMedico:
    """Estructura de datos para un centro médico"""
    nombre: str
    tipo: str
    direccion: str
    telefono: str
    especialidades: List[str]
    lat: float
    lng: float
    horarios: str = ""
    calificacion: float = 0.0
    sitio_web: str = ""
    distancia_km: float = 0.0

class AgenteBusquedaCentros(Agente):
    def __init__(self):
        load_dotenv()
        
        config = {
            "nombre": "Agente Búsqueda de Centros",
            "tipo": "geolocalizacion"
        }

        model_config = {
            "model_path": os.getenv("MODEL_PATH"),
            "n_threads": int(os.getenv("LLAMA_N_THREADS", os.cpu_count() or 8)),
            "n_batch": int(os.getenv("LLAMA_N_BATCH", 256)),
            "n_ctx": int(os.getenv("LLAMA_N_CTX", 2048)),
            "temperature": 0.3, 
            "max_tokens": 512,
            "verbose": True
        }

        prompt_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "prompts",
            "busqueda_centros.txt"
        )

        super().__init__(
            config=config,
            model_config=model_config,
            system_prompt_path=prompt_path
        )
        
        # Configuración de APIs
        self.google_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.nominatim_url = "https://nominatim.openstreetmap.org"
        self.overpass_url = "https://overpass-api.de/api/interpreter"
        
        # Base de datos local de centros médicos (backup)
        self.centros_locales = self._cargar_centros_locales()
        
        # Patrones para extraer información de la consulta
        self.patrones_busqueda = {
            'especialidades': [
                r'\b(cardiología|cardiólogo|corazón)\b',
                r'\b(neurología|neurólogo|cerebro|nervioso)\b',
                r'\b(dermatología|dermatólogo|piel)\b',
                r'\b(pediatría|pediatra|niños|bebés)\b',
                r'\b(ginecología|ginecólogo|mujer|embarazo)\b',
                r'\b(traumatología|traumatólogo|huesos|fracturas)\b',
                r'\b(oftalmología|oftalmólogo|ojos|vista)\b',
                r'\b(psiquiatría|psiquiatra|mental|depresión)\b',
                r'\b(radiología|rayos\s*x|tomografía|resonancia)\b',
                r'\b(laboratorio|análisis|exámenes)\b',
                r'\b(urgencias|emergencias|24\s*horas)\b'
            ],
            'tipos_centro': [
                r'\b(hospital|centro\s*médico|clínica|policlínico)\b',
                r'\b(eps|ips|seguro\s*social)\b',
                r'\b(privado|particular)\b',
                r'\b(público|estatal)\b'
            ],
            'ubicacion': [
                r'\bcerca\s*de\s*([^,\.]+)\b',
                r'\ben\s*([^,\.]+)\b',
                r'\bbarrio\s*([^,\.]+)\b',
                r'\bzona\s*([^,\.]+)\b'
            ]
        }
    
    def _cargar_centros_locales(self) -> List[CentroMedico]:
        """Carga base de datos local de centros médicos"""
        # Base de datos de ejemplo para Medellín, Colombia
        centros = [
            CentroMedico(
                nombre="Hospital Pablo Tobón Uribe",
                tipo="Hospital Privado",
                direccion="Calle 78B #69-240, Medellín",
                telefono="(604) 445-9000",
                especialidades=["Cardiología", "Neurología", "Oncología", "Cirugía", "Urgencias"],
                lat=6.2648,
                lng=-75.5890,
                horarios="24 horas",
                calificacion=4.5,
                sitio_web="https://www.hptu.org.co"
            ),
            CentroMedico(
                nombre="Hospital General de Medellín",
                tipo="Hospital Público",
                direccion="Carrera 48 #32-102, Medellín",
                telefono="(604) 385-5555",
                especialidades=["Medicina General", "Urgencias", "Pediatría", "Ginecología"],
                lat=6.2442,
                lng=-75.5812,
                horarios="24 horas",
                calificacion=3.8
            ),
            CentroMedico(
                nombre="Clínica Las Vegas",
                tipo="Clínica Privada",
                direccion="Calle 2 Sur #46-55, Medellín",
                telefono="(604) 342-1010",
                especialidades=["Cardiología", "Dermatología", "Oftalmología", "Laboratorio"],
                lat=6.2077,
                lng=-75.5761,
                horarios="Lun-Vie: 7:00-19:00, Sab: 8:00-14:00",
                calificacion=4.2
            ),
            CentroMedico(
                nombre="Hospital San Vicente Fundación",
                tipo="Hospital Universitario",
                direccion="Calle 64 #51D-154, Medellín",
                telefono="(604) 444-1333",
                especialidades=["Todas las especialidades", "Urgencias", "Transplantes", "Investigación"],
                lat=6.2518,
                lng=-75.5636,
                horarios="24 horas",
                calificacion=4.3,
                sitio_web="https://www.sanvicentefundacion.com"
            ),
            CentroMedico(
                nombre="Centro Médico Imbanaco Medellín",
                tipo="Centro Médico Privado",
                direccion="Carrera 43A #1A Sur-145, Medellín",
                telefono="(604) 305-5555",
                especialidades=["Medicina General", "Especialistas", "Laboratorio", "Imágenes"],
                lat=6.2033,
                lng=-75.5677,
                horarios="Lun-Vie: 6:00-20:00, Sab: 7:00-15:00",
                calificacion=4.0
            ),
            CentroMedico(
                nombre="Clínica Medellín",
                tipo="Clínica Privada",
                direccion="Carrera 46 #19B-42, Medellín",
                telefono="(604) 250-8000",
                especialidades=["Cardiología", "Neurocirugía", "Ortopedia", "Oncología"],
                lat=6.2094,
                lng=-75.5712,
                horarios="24 horas",
                calificacion=4.4
            )
        ]
        return centros
    
    def _calcular_distancia(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calcula distancia entre dos puntos usando fórmula de Haversine"""
        # Convertir a radianes
        lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
        
        # Fórmula de Haversine
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
        c = 2 * asin(sqrt(a))
        
        # Radio de la Tierra en kilómetros
        r = 6371
        return c * r
    
    def _obtener_coordenadas_direccion(self, direccion: str) -> Optional[Tuple[float, float]]:
        """Obtiene coordenadas de una dirección usando Nominatim (OpenStreetMap)"""
        try:
            # Agregar contexto de Colombia/Medellín si no está especificado
            if "colombia" not in direccion.lower() and "medellín" not in direccion.lower():
                direccion += ", Medellín, Colombia"
            
            params = {
                'q': direccion,
                'format': 'json',
                'limit': 1
            }
            
            headers = {
                'User-Agent': 'AgenteMedico/1.0'
            }
            
            response = requests.get(self.nominatim_url + "/search", params=params, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    return float(data[0]['lat']), float(data[0]['lon'])
            
        except Exception as e:
            print(f"[BUSQUEDA] Error obteniendo coordenadas: {str(e)}")
        
        return None
    
    def _extraer_parametros_busqueda(self, mensaje: str) -> Dict:
        """Extrae parámetros de búsqueda del mensaje del usuario"""
        mensaje_lower = mensaje.lower()
        parametros = {
            'especialidades': [],
            'tipos_centro': [],
            'ubicacion': None,
            'radio_km': 10  
        }
        
        # Extraer especialidades
        especialidades_map = {
            'cardiología': ['cardiología', 'cardiólogo', 'corazón'],
            'neurología': ['neurología', 'neurólogo', 'cerebro', 'nervioso'],
            'dermatología': ['dermatología', 'dermatólogo', 'piel'],
            'pediatría': ['pediatría', 'pediatra', 'niños', 'bebés'],
            'ginecología': ['ginecología', 'ginecólogo', 'mujer', 'embarazo'],
            'traumatología': ['traumatología', 'traumatólogo', 'huesos', 'fracturas'],
            'oftalmología': ['oftalmología', 'oftalmólogo', 'ojos', 'vista'],
            'psiquiatría': ['psiquiatría', 'psiquiatra', 'mental', 'depresión'],
            'radiología': ['radiología', 'rayos x', 'tomografía', 'resonancia'],
            'laboratorio': ['laboratorio', 'análisis', 'exámenes'],
            'urgencias': ['urgencias', 'emergencias', '24 horas']
        }
        
        for especialidad, palabras_clave in especialidades_map.items():
            if any(palabra in mensaje_lower for palabra in palabras_clave):
                parametros['especialidades'].append(especialidad)
        
        # Extraer tipos de centro
        if any(palabra in mensaje_lower for palabra in ['hospital']):
            parametros['tipos_centro'].append('hospital')
        if any(palabra in mensaje_lower for palabra in ['clínica', 'clinica']):
            parametros['tipos_centro'].append('clínica')
        if any(palabra in mensaje_lower for palabra in ['privado', 'particular']):
            parametros['tipos_centro'].append('privado')
        if any(palabra in mensaje_lower for palabra in ['público', 'publico', 'estatal']):
            parametros['tipos_centro'].append('público')
        
        # Extraer ubicación
        patrones_ubicacion = [
            r'\bcerca\s*de\s*([^,\.!?]+)',
            r'\ben\s*el?\s*([^,\.!?]+)',
            r'\bbarrio\s*([^,\.!?]+)',
            r'\bzona\s*([^,\.!?]+)'
        ]
        
        for patron in patrones_ubicacion:
            match = re.search(patron, mensaje_lower)
            if match:
                parametros['ubicacion'] = match.group(1).strip()
                break
        
        # Extraer radio de búsqueda
        radio_match = re.search(r'(\d+)\s*km', mensaje_lower)
        if radio_match:
            parametros['radio_km'] = int(radio_match.group(1))
        
        return parametros
    
    def _filtrar_centros(self, centros: List[CentroMedico], parametros: Dict) -> List[CentroMedico]:
        """Filtra centros médicos según los parámetros de búsqueda"""
        centros_filtrados = []
        
        for centro in centros:
            # Filtrar por especialidades
            if parametros['especialidades']:
                especialidades_centro = [esp.lower() for esp in centro.especialidades]
                if not any(esp in ' '.join(especialidades_centro) for esp in parametros['especialidades']):
                    continue
            
            # Filtrar por tipo de centro
            if parametros['tipos_centro']:
                tipo_centro_lower = centro.tipo.lower()
                tipo_coincide = False
                
                for tipo_filtro in parametros['tipos_centro']:
                    if tipo_filtro in tipo_centro_lower:
                        tipo_coincide = True
                        break
                
                if not tipo_coincide:
                    continue
            
            centros_filtrados.append(centro)
        
        return centros_filtrados
    
    def _ordenar_por_distancia(self, centros: List[CentroMedico], lat_usuario: float, lng_usuario: float) -> List[CentroMedico]:
        """Ordena centros por distancia al usuario"""
        for centro in centros:
            centro.distancia_km = self._calcular_distancia(
                lat_usuario, lng_usuario, centro.lat, centro.lng
            )
        
        return sorted(centros, key=lambda x: x.distancia_km)
    
    def _formatear_respuesta(self, centros: List[CentroMedico], parametros: Dict) -> str:
        """Formatea la respuesta con los centros encontrados"""
        if not centros:
            return ("🏥 No se encontraron centros médicos que coincidan con tu búsqueda. "
                   "Intenta ampliar los criterios o verificar la ubicación.")
        
        respuesta = "🏥 **Centros Médicos Encontrados:**\n\n"
        
        # Agregar información de búsqueda
        if parametros['especialidades']:
            respuesta += f"🔍 **Especialidades:** {', '.join(parametros['especialidades']).title()}\n"
        if parametros['ubicacion']:
            respuesta += f"📍 **Cerca de:** {parametros['ubicacion'].title()}\n"
        respuesta += f"📏 **Radio de búsqueda:** {parametros['radio_km']} km\n\n"
        
        # Listar centros (máximo 5)
        for i, centro in enumerate(centros[:5], 1):
            respuesta += f"**{i}. {centro.nombre}**\n"
            respuesta += f"   🏢 *{centro.tipo}*\n"
            respuesta += f"   📍 {centro.direccion}\n"
            respuesta += f"   📞 {centro.telefono}\n"
            
            if centro.distancia_km > 0:
                respuesta += f"   📏 {centro.distancia_km:.1f} km de distancia\n"
            
            if centro.especialidades:
                especialidades_str = ", ".join(centro.especialidades[:3])
                if len(centro.especialidades) > 3:
                    especialidades_str += f" y {len(centro.especialidades) - 3} más"
                respuesta += f"   🩺 {especialidades_str}\n"
            
            if centro.horarios:
                respuesta += f"   🕒 {centro.horarios}\n"
            
            if centro.calificacion > 0:
                respuesta += f"   ⭐ {centro.calificacion}/5.0\n"
            
            if centro.sitio_web:
                respuesta += f"   🌐 {centro.sitio_web}\n"
            
            respuesta += "\n"
        
        # Pie de página
        if len(centros) > 5:
            respuesta += f"... y {len(centros) - 5} centros más encontrados.\n\n"
        
        respuesta += ("💡 **Consejos:**\n"
                     "• Llama antes de ir para confirmar horarios y disponibilidad\n"
                     "• Pregunta por tu EPS/seguro médico\n"
                     "• En emergencias, dirígete al centro más cercano con urgencias")
        
        return respuesta
    
    def iniciar_interaccion(self, session_id: str, mensaje: str) -> Optional[Dict]:
        """Inicia la interacción con el agente de búsqueda de centros"""
        print(f"[BUSQUEDA_CENTROS] Iniciando interacción para sesión {session_id}")
        
        # Extraer parámetros de búsqueda del mensaje inicial
        parametros = self._extraer_parametros_busqueda(mensaje)
        
        return {
            "parametros_busqueda": parametros,
            "centros_disponibles": len(self.centros_locales),
            "apis_disponibles": {
                "google_maps": bool(self.google_api_key),
                "nominatim": True
            }
        }
    
    def preguntar(self, session_id: str, pregunta: str, metadata: Optional[Dict] = None) -> Dict:
        """Procesa consulta de búsqueda de centros médicos"""
        try:
            # Extraer parámetros de búsqueda
            parametros = self._extraer_parametros_busqueda(pregunta)
            
            # Obtener coordenadas del usuario si se especifica ubicación
            lat_usuario, lng_usuario = 6.2442, -75.5812  
            
            if parametros['ubicacion']:
                coords = self._obtener_coordenadas_direccion(parametros['ubicacion'])
                if coords:
                    lat_usuario, lng_usuario = coords
                    print(f"[BUSQUEDA] Coordenadas obtenidas: {lat_usuario}, {lng_usuario}")
                else:
                    print(f"[BUSQUEDA] No se pudieron obtener coordenadas para: {parametros['ubicacion']}")
            
            # Filtrar centros según criterios
            centros_filtrados = self._filtrar_centros(self.centros_locales, parametros)
            
            # Filtrar por distancia
            centros_en_radio = []
            for centro in centros_filtrados:
                distancia = self._calcular_distancia(lat_usuario, lng_usuario, centro.lat, centro.lng)
                if distancia <= parametros['radio_km']:
                    centro.distancia_km = distancia
                    centros_en_radio.append(centro)
            
            # Ordenar por distancia
            centros_ordenados = self._ordenar_por_distancia(centros_en_radio, lat_usuario, lng_usuario)
            
            # Formatear respuesta
            respuesta = self._formatear_respuesta(centros_ordenados, parametros)
            
            return {
                "output": respuesta,
                "metadata": {
                    "tipo": "busqueda_centros",
                    "centros_encontrados": len(centros_ordenados),
                    "parametros_busqueda": parametros,
                    "coordenadas_usuario": [lat_usuario, lng_usuario]
                }
            }
            
        except Exception as e:
            error_msg = f"Error en búsqueda de centros: {str(e)}"
            print(f"[ERROR BUSQUEDA] {error_msg}")
            
            return {
                "output": f"❌ {error_msg}\n\nPor favor, intenta reformular tu búsqueda.",
                "metadata": {"tipo": "error", "error": error_msg}
            }
    
    def buscar_por_especialidad(self, session_id: str, especialidad: str, ubicacion: str = None) -> Dict:
        """Método específico para buscar por especialidad"""
        consulta = f"Buscar {especialidad}"
        if ubicacion:
            consulta += f" cerca de {ubicacion}"
        
        return self.preguntar(session_id, consulta)
    
    def buscar_urgencias(self, session_id: str, ubicacion: str = None) -> Dict:
        """Método específico para buscar centros de urgencias"""
        consulta = "Buscar urgencias 24 horas"
        if ubicacion:
            consulta += f" cerca de {ubicacion}"
        
        return self.preguntar(session_id, consulta)
    
    def obtener_direcciones(self, session_id: str, nombre_centro: str) -> Dict:
        """Obtiene direcciones detalladas a un centro específico"""
        # Buscar el centro en la base de datos local
        centro_encontrado = None
        for centro in self.centros_locales:
            if nombre_centro.lower() in centro.nombre.lower():
                centro_encontrado = centro
                break
        
        if not centro_encontrado:
            return {
                "output": f"❌ No se encontró información para '{nombre_centro}'",
                "metadata": {"tipo": "error"}
            }
        
        respuesta = f"🗺️ **Direcciones a {centro_encontrado.nombre}:**\n\n"
        respuesta += f"📍 **Dirección:** {centro_encontrado.direccion}\n"
        respuesta += f"📞 **Teléfono:** {centro_encontrado.telefono}\n"
        respuesta += f"🕒 **Horarios:** {centro_encontrado.horarios}\n\n"
        respuesta += "🚗 **Opciones de transporte:**\n"
        respuesta += "• En vehículo particular o taxi\n"
        respuesta += "• Transporte público (verificar rutas)\n"
        respuesta += "• Aplicaciones de transporte (Uber, InDriver, etc.)\n\n"
        respuesta += f"🌐 Para direcciones precisas, puedes usar Google Maps con la dirección: {centro_encontrado.direccion}"
        
        return {
            "output": respuesta,
            "metadata": {
                "tipo": "direcciones",
                "centro": centro_encontrado.nombre,
                "coordenadas": [centro_encontrado.lat, centro_encontrado.lng]
            }
        }