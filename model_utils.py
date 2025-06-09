import os
from ultralytics import YOLO
from PIL import Image
import numpy as np

# General object detection-model (YOLOv8n)
model_general = YOLO('yolov8n.pt')

# Path til din finetunede mad-model
food_model_path = 'models/food_model.pt'
if os.path.exists(food_model_path):
    model_food = YOLO(food_model_path)
else:
    model_food = None
    print(f"[Warning] Mad-model ikke fundet på {food_model_path}. Mad-genkendelse deaktiveret.")

def detect_objects(img: Image.Image):
    """Returnér liste af detektioner (hånd, skål, etc.)."""
    results = model_general.predict(source=np.array(img), verbose=False)[0]
    boxes = results.boxes.xyxy.cpu().numpy()
    confs = results.boxes.conf.cpu().numpy()
    classes = results.boxes.cls.cpu().numpy().astype(int)
    names = [results.names[c] for c in classes]

    detections = []
    for i, ((x1, y1, x2, y2), conf, cls, name) in enumerate(zip(boxes, confs, classes, names)):
        detections.append({
            'xmin': float(x1), 'ymin': float(y1),
            'xmax': float(x2), 'ymax': float(y2),
            'confidence': float(conf),
            'class': int(cls),
            'name': name
        })
    return detections

def detect_food_items(img: Image.Image, crop_boxes):
    """Genkend madvarer i de givne bokse, hvis mad-model er tilgængelig."""
    if model_food is None:
        return []
    foods = []
    for box in crop_boxes:
        crop = img.crop((box['xmin'], box['ymin'], box['xmax'], box['ymax']))
        res = model_food.predict(source=np.array(crop), verbose=False)[0]
        if res.boxes and len(res.boxes.cls) > 0:
            cls = int(res.boxes.cls.cpu().numpy()[0])
            name = res.names[cls]
            foods.append(name)
    return foods
