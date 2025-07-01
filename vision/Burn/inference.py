import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights
from PIL import Image

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],  # ImageNet mean
                         [0.229, 0.224, 0.225])  # ImageNet std
])

def load_model(path='model.pt'):
    weights = EfficientNet_B0_Weights.DEFAULT
    model = efficientnet_b0(weights=weights)

    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, 3)

    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    model.eval()

    return model

def preprocess_image(image_path):
    image = Image.open(image_path).convert('RGB')
    return transform(image).unsqueeze(0)


def workflow(image_path, class_names=["Grado 1", "Grado 2", "Grado 3"]):

    model = load_model()
    input_tensor = preprocess_image(image_path)

    with torch.no_grad():
        outputs = model(input_tensor)
        probs = torch.softmax(outputs, dim=1)
        predicted_idx = torch.argmax(probs, dim=1).item()
        confidence = probs[0][predicted_idx].item()

        return class_names[predicted_idx], confidence, probs # Grado clasificado, confidencia y vector de probabilidades
