import streamlit as st
import requests

st.title("🌾 Smart Crop Recommendation")

temp = st.slider("Temperature (°C)", 10, 45, 25)
rain = st.slider("Rainfall (mm)", 0, 3000, 600)
season = st.selectbox("Season", ["Kharif", "Rabi", "Zaid"])

if st.button("Recommend"):
    URL = "http://127.0.0.1:8000/recommend"
    params = {"temp": temp, "rain": rain, "season": season}

    response = requests.get(URL, params=params)

    if response.status_code != 200:
        st.error("API Error")
        st.code(response.text)
    else:
        data = response.json()
        st.success("Top 3 Recommended Crops")

        for i, crop in enumerate(data, 1):
            st.write(f"{i}. 🌱 {crop['crop']} — Score: {crop['score']}")
