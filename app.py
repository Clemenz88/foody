import streamlit as st
from PIL import Image
import pandas as pd
from model_utils import detect_objects, detect_food_items
from volume_estimation import estimate_volume
from calorie_lookup import lookup_calories

st.title("📸 Madkalorie-estimator med hånd-reference")

uploaded = st.file_uploader("Upload et billede af din mad med hånden som reference", type=["jpg","png"])
hand_size = st.number_input("Håndbredde i cm (mål tværs over knoerne)", min_value=5.0, max_value=30.0, value=8.5)

# Indlæs kalorie-database for fallback
df_cal = pd.read_csv('data/food_calories.csv')
fallback_options = ['-- Intet --'] + df_cal['food'].tolist()
fallback = st.selectbox("Vælg madvare manuelt", fallback_options)
fallback_volume = st.slider("Volume/vægt (ml/gram)", 10, 1000, 100)

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    detections = detect_objects(img)  # liste af dicts

    # Find hånd
    hand_dets = [d for d in detections if d['name'] == 'hand']
    if not hand_dets:
        st.error("Kunne ikke genkende en hånd i billedet. Sørg for at hånden er synlig.")
    else:
        hand_box = hand_dets[0]

        # Find mad-beholdere
        food_boxes = [d for d in detections if d['name'] in ['bowl', 'plate', 'cup']]
        results = []
        for fb in food_boxes:
            vol = estimate_volume(hand_box, fb, hand_size)
            foods = detect_food_items(img, [fb])
            for food in foods:
                kcal = lookup_calories(food, vol)
                results.append((food, vol, kcal))

        if results:
            st.header("Resultater")
            for food, vol, kcal in results:
                st.write(f"- **{food}**: {vol:.0f} ml → ca. **{kcal:.0f} kcal**")
        else:
            st.warning("Kunne ikke genkende mad på billedet. Brug venligst dropdown nedenfor.")

# Håndter fallback
if fallback and fallback != '-- Intet --':
    kcal_fb = lookup_calories(fallback, fallback_volume)
    st.info(f"Fallback: **{fallback}**; volumen {fallback_volume} ml → **{kcal_fb:.0f} kcal**")

st.markdown("---")
st.write("Feedback / læringsmulighed kommer snart…")
