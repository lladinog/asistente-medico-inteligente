from ultralytics import YOLO


def load_yolo_model():
    model = YOLO('/workspaces/asistente-medico-inteligente/vision/Brain Tumor/model.pt')
    return model

def workflow(image_path):
    model = load_yolo_model()
    return model(image_path)

    # El resultado es un iterable con:
        # Diccionario de clases
        # Clases predichas
        # Niveles de confianza
        # coordenadas de los bounding boxes (x1, y1, x2, y2)