import os
import sys
import numpy as np
import pandas as pd
from glob import glob

from keras.applications.mobilenet import MobileNet
from keras.layers import GlobalAveragePooling2D, Dense, Dropout
from keras.models import Sequential
from keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator

# === Parámetros de tu entrenamiento ===
IMG_SIZE = (128, 128)
WEIGHTS_PATH = 'xray_class_weights.best.hdf5'
CSV_PATH = '../input/Data_Entry_2017.csv'  # ruta al CSV original
MIN_CASES = 1000

# === 1. Reconstruir lista de clases ===
def get_class_names(csv_path, min_cases=MIN_CASES):
    df = pd.read_csv(csv_path)
    # extraemos todas las etiquetas
    all_labels = []
    for s in df['Finding Labels']:
        for lab in s.split('|'):
            if lab and lab not in all_labels:
                all_labels.append(lab)
    # filtramos las que aparecen al menos min_cases veces
    valid = []
    for lab in all_labels:
        if (df['Finding Labels'].str.contains(fr'\b{lab}\b')).sum() >= min_cases:
            valid.append(lab)
    return sorted(valid)

CLASS_NAMES = get_class_names(CSV_PATH)

# === 2. Reconstruir el modelo ===
def build_model(num_classes=len(CLASS_NAMES)):
    base = MobileNet(input_shape=IMG_SIZE + (1,),
                     include_top=False,
                     weights=None)  # entrenaste sin pesos de ImageNet
    model = Sequential([
        base,
        GlobalAveragePooling2D(),
        Dropout(0.5),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='sigmoid')
    ])
    return model

# === 3. Cargar pesos y compilar ===
model = build_model()
model.load_weights(WEIGHTS_PATH)
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['binary_accuracy'])

# === 4. Preparar generador sólo para normalización sample-wise ===
datagen = ImageDataGenerator(
    samplewise_center=True,
    samplewise_std_normalization=True
)

def preprocess_image(path):
    # carga en escala de grises
    img = load_img(path, color_mode='grayscale', target_size=IMG_SIZE)
    x = img_to_array(img)                # (128,128,1)
    x = np.expand_dims(x, 0)             # batch (1,128,128,1)
    x = datagen.standardize(x)           # same normalization as en entrenamiento
    return x

# === 5. Función de inferencia ===
def infer_image(path):
    x = preprocess_image(path)
    preds = model.predict(x)[0]          # vector de probabilidades
    # emparejamos cada clase con su score
    results = list(zip(CLASS_NAMES, preds))
    # orden descendente por probabilidad
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def workflow(image_path):
    res = infer_image(image_path)
    
    for cls, score in res[:5]:  # top‑5
        print(f"  {cls:20s}: {score:.2%}")
