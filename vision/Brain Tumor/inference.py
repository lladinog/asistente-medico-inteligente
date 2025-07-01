from ultralytics import YOLO
import sys
import cv2

# ===== 1. Cargar el modelo YOLO (puede ser yolov8n.pt, yolov8s.pt o personalizado) =====
def load_yolo_model(model_path='model.pt'):
    model = YOLO(model_path)  # Puedes usar 'best.pt' si es un modelo entrenado por ti
    return model

# ===== 2. Realizar inferencia sobre una imagen =====
def infer_image(model, image_path):
    results = model(image_path)
    
    # Mostrar resultados en consola
    for result in results:
        print(result.names)  # diccionario de clases
        print(result.boxes.cls)  # clases predichas
        print(result.boxes.conf)  # niveles de confianza
        print(result.boxes.xyxy)  # coordenadas de los bounding boxes (x1, y1, x2, y2)

    # Mostrar imagen con resultados
    results[0].show()  # abre una ventana con la imagen y las predicciones
    # results[0].save(filename="resultado.jpg")  # opcional: guarda el resultado

# ===== 3. Main =====
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Uso: python inferencia_yolo.py modelo.pt imagen.jpg")
        sys.exit(1)

    model_path = sys.argv[1]
    image_path = sys.argv[2]

    model = load_yolo_model(model_path)
    infer_image(model, image_path)
