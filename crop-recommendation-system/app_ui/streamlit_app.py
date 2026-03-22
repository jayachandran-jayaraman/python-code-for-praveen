import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Smart Crop AI", layout="centered")

st.title("🌾 Smart Crop Recommendation (AI Powered)")

st.subheader("🌱 Soil & Weather Inputs")

# Inputs
N = st.number_input("Nitrogen (N)", 0, 150, 50)
P = st.number_input("Phosphorus (P)", 0, 150, 50)
K = st.number_input("Potassium (K)", 0, 150, 50)

temperature = st.slider("🌡 Temperature (°C)", 10, 45, 25)
humidity = st.slider("💧 Humidity (%)", 10, 100, 60)
ph = st.slider("⚗️ Soil pH", 3.5, 9.0, 6.5)
rainfall = st.slider("🌧 Rainfall (mm)", 0, 3000, 600)

# Predict
if st.button("🚀 Predict Crop"):
    try:
        res = requests.get(
            "http://127.0.0.1:8000/predict",
            params={
                "N": N,
                "P": P,
                "K": K,
                "temperature": temperature,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall
            }
        )

        data = res.json()

        st.success(f"🌱 Best Crop: {data['prediction']}")

        st.subheader("🏆 Top 3 Recommendations")

        df = pd.DataFrame(data["top3"])
        st.bar_chart(df.set_index("crop"))

    except Exception as e:
        st.error("Server error")
        st.code(str(e))