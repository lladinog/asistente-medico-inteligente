from inference import workflow

results = workflow("https://ultralytics.com/assets/brain-tumor-sample.jpg")

for result in results:
    print(f"Classification: {'positive' if bool(result.boxes.cls[0].item()) else 'negative'}")  # clases predichas
    print(f'Prob: {result.boxes.conf[0].item()}')  # niveles de confianza