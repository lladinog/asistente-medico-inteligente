from ultralytics import YOLO
import os


def load_yolo_model():
    model_path = os.path.join(os.path.dirname(__file__), 'model.pt')
    model = YOLO(model_path)
    return model

def workflow(image_path):
    model = load_yolo_model()
    return model(image_path)

    # El resultado es un iterable con:
        # Diccionario de clases
        # Clases predichas
        # Niveles de confianza
        # coordenadas de los bounding boxes (x1, y1, x2, y2)