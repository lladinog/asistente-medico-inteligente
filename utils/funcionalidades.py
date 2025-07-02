from enum import Enum

class FuncionalidadMedica(Enum):
    DIAGNOSTICO = ("diagnostico", "🔍", "Diagnóstico médico")
    ANALISIS_IMAGENES = ("analisis_imagenes", "🖼️", "Análisis de imágenes")
    INTERPRETACION_EXAMENES = ("interpretacion_examenes", "🔬", "Interpretación de exámenes")
    EXPLICACION = ("explicacion", "📚", "Explicación médica")
    BUSCADOR_CENTROS = ("buscador_centros", "🏥", "Buscador de centros médicos")
    CONTACTO_MEDICO = ("contacto_medico", "👨‍⚕️", "Contacto médico")

    @property
    def key(self):
        return self.value[0]

    @property
    def emoji(self):
        return self.value[1]

    @property
    def label(self):
        return self.value[2]

