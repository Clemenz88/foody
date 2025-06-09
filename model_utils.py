import torch
from PIL import Image
import numpy as np

# Indlæs general object detection-model (f.eks. YOLOv5)
model_general = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
# Indlæs specifik mad-model (skal trænes/finetunes separat)
model_food = torch.hub.load('ultralytics/yolov5', 'custom', path='path/to/your/food_model.pt')

def detect_objects(img: Image.Image):
    """Returnér detektioner for hånd, skål, etc."""
    results = model_general(img)
    return results.pandas().xyxy[0]

def detect_food_items(img: Image.Image, crop_boxes):
    """Given crops around madobjekter, genkend præcis madvare."""
    foods = []
    for box in crop_boxes:
        crop = img.crop((box['xmin'], box['ymin'], box['xmax'], box['ymax']))
        res = model_food(crop)
        pred = res.pandas().xyxy[0]
        if not pred.empty:
            foods.append(pred.iloc[0]['name'])
    return foods
