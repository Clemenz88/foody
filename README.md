# Food Calorie App

Denne applikation estimerer kalorier i mad på et billede ved hjælp af en hånd som reference.

## Funktioner

- Objektgenkendelse af hånd og madbeholder
- Volumenestimering baseret på håndens størrelse
- Genkendelse af madvarer med en finjusteret model
- Kalorieopslag fra en lokal database
- Fallback-menu med hyppige madvarer
- Mulighed for løbende feedback/læring

## Installation

1. Clone repositoriet:
    git clone https://github.com/<YOUR_USERNAME>/food_calorie_app.git
    cd food_calorie_app
    pip install -r requirements.txt

## Kørsel lokalt

    streamlit run app.py

## Deployment

1. Push til GitHub.
2. Link repositoriet på Streamlit Cloud: https://share.streamlit.io
