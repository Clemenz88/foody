import streamlit as st
from PIL import Image
from model_utils import detect_objects, detect_food_items
from volume_estimation import estimate_volume
from calorie_lookup import lookup_calories

st.title("📸 Madkalorie-estimator med hånd-reference")

uploaded = st.file_uploader("Upload et billede af din mad med hånden som reference", type=["jpg","png"])
hand_size = st.number_input("Håndbredde i cm (mål tværs over knoerne)", min_value=5.0, max_value=30.0, value=8.5)

fallback = st.selectbox("Vælg madvare manuelt", ["-- Intet --"] + list(open('data/food_calories.csv').read().splitlines()[1:]))
fallback_volume = st.slider("Volume/vægt (ml/gram)", 10, 1000, 100)

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    detections = detect_objects(img)

    hand_box = detections[detections['name']=='hand'].iloc[0].to_dict()
    food_boxes = detections[detections['name'].isin(['bowl','plate','cup'])]

    results = []
    for _, fb in food_boxes.iterrows():
        vol = estimate_volume(hand_box, fb.to_dict(), hand_size)
        foods = detect_food_items(img, [fb.to_dict()])
        for food in foods:
            kcal = lookup_calories(food, vol)
            results.append((food, vol, kcal))
    if results:
        st.header("Resultater")
        for food, vol, kcal in results:
            st.write(f"- **{food}**: {vol:.0f} ml → ca. **{kcal:.0f} kcal**")
    else:
        st.warning("Kunne ikke genkende mad på billedet. Brug venligst dropdown nederst.")

if fallback and fallback != "-- Intet --":
    kcal_fb = lookup_calories(fallback, fallback_volume)
    st.info(f"Fallback: **{fallback}**; volumen {fallback_volume} ml → **{kcal_fb:.0f} kcal**")

st.markdown("---")
st.write("Feedback / læringsmulighed kommer snart…")
