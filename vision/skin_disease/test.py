from inference import workflow
import os

print(workflow(os.path.join(os.path.dirname(__file__), "ISIC_0029328.jpg")))