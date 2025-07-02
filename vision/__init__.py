from langchain.tools import tool

from vision.brain_tumor import BrainTumorProcess
from vision.burn import BurnProcess
from vision.chest_x_rays import ChestXRayProcess
from vision.skin_disease import SkinDiseaseProcess


@tool
def analizar_tumor_cerebral(image_path: str) -> str:
    """Detecta la presencia de tumores cerebrales en imágenes médicas."""
    return BrainTumorProcess(image_path)

@tool
def analizar_quemaduras(image_path: str) -> str:
    """Clasifica el nivel de quemadura en una imagen."""
    return BurnProcess(image_path)

@tool
def analizar_radiografia_torax(image_path: str) -> str:
    """Analiza una radiografía de tórax para detectar anomalías."""
    return ChestXRayProcess(image_path)

@tool
def analizar_enfermedad_piel(image_path: str) -> str:
    """Detecta enfermedades cutáneas a partir de una imagen."""
    return SkinDiseaseProcess(image_path)

__all__ = [
    "analizar_tumor_cerebral",
    "analizar_quemaduras",
    "analizar_radiografia_torax",
    "analizar_enfermedad_piel"
]