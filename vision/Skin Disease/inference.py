import sys
import numpy as np
from tensorflow.keras.models import load_model
from cv2 import imread, resize

TARGET_SIZE = (28, 28)

classes = {
    4: ('nv', ' melanocytic nevi'),
    6: ('mel', 'melanoma'),
    2 :('bkl', 'benign keratosis-like lesions'),
    1:('bcc' , ' basal cell carcinoma'),
    5: ('vasc', ' pyogenic granulomas and hemorrhage'),
    0: ('akiec', 'Actinic keratoses and intraepithelial carcinomae'),
    3: ('df', 'dermatofibroma')
}

def preprocess_image(img_path):
    img = imread(img_path)
    img = resize(img, TARGET_SIZE)
    return img.reshape(1, TARGET_SIZE[0], TARGET_SIZE[1], 3).astype('float32')

def workflow(image_path):

    model = load_model('model.h5')

    img_preprocessed = preprocess_image(image_path)
    pred = model.predict(img_preprocessed)

    # Mostrar predicción
    predicted_class = np.argmax(pred, axis=1)[0]
    print(f"Predicción: Clase {classes[predicted_class]} - Probabilidades: {pred[0]}")