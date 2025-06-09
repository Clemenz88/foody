import numpy as np

def estimate_volume(hand_box, food_box, hand_real_width_cm):
    """
    Estimér volumen baseret på pixelmål.
    - hand_box: dict med pixel-bredde for hånd (xmin→xmax)
    - food_box: dict med pixel-område for madobjekt
    - hand_real_width_cm: brugerinput
    """
    hand_px_width = hand_box['xmax'] - hand_box['xmin']
    px_to_cm = hand_real_width_cm / hand_px_width

    w_px = food_box['xmax'] - food_box['xmin']
    h_px = food_box['ymax'] - food_box['ymin']
    w_cm, h_cm = w_px * px_to_cm, h_px * px_to_cm

    volume_ml = w_cm * w_cm * h_cm  # ml ~ cm³
    return volume_ml
