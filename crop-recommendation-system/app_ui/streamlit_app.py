import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(page_title="Smart Crop AI", layout="wide")

# ==========================
# MINT UI THEME
# ==========================
st.markdown("""
<style>
    .stApp {
        background-color: #f0fffb;
    }

    h1, h2, h3 {
        color: #0f766e;
        text-align: center;
    }

    .stButton>button {
        background-color: #14b8a6;
        color: white;
        border-radius: 10px;
        padding: 10px;
        border: none;
        font-weight: bold;
        width: 100%;
    }

    .stButton>button:hover {
        background-color: #0d9488;
    }

    section[data-testid="stSidebar"] {
        background-color: #ccfbf1;
    }

    .block-container {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================
# CUSTOM NAVIGATION (NO DEFAULT ACTIVE BUG)
# ==========================
st.sidebar.title("Navigation")

if "page" not in st.session_state:
    st.session_state.page = "Home"

def nav(label):
    if st.sidebar.button(label):
        st.session_state.page = label

nav("Home")
nav("Crop Analysis")

page = st.session_state.page

# ==========================
# WEATHER FUNCTION
# ==========================
def get_live_weather():
    try:
        res = requests.get("https://wttr.in/?format=j1", timeout=5).json()
        cur = res["current_condition"][0]

        return (
            float(cur["temp_C"]),
            float(cur["humidity"]),
            float(cur.get("precipMM", 0)) * 10
        )
    except:
        return None, None, None

# ==========================
# DEFAULT STATE
# ==========================
if "weather" not in st.session_state:
    st.session_state.weather = {"temp": 25, "humidity": 60, "rain": 500}

if "soil" not in st.session_state:
    st.session_state.soil = {"N": 50, "P": 50, "K": 50, "ph": 6.5}

# ==========================
# HOME PAGE
# ==========================
if page == "Home":

    st.title("Smart Crop Recommendation System")

    # Top Buttons
    col1, col2, col3 = st.columns(3)

    # Weather Fetch
    if col1.button("Fetch Weather"):
        temp, humidity, rain = get_live_weather()

        if temp:
            st.session_state.weather = {
                "temp": int(temp),
                "humidity": int(humidity),
                "rain": int(rain)
            }
            st.success("Weather updated")
        else:
            st.error("Weather fetch failed")

    # Auto Recommend
    if col2.button("Auto Recommend"):
        try:
            soil = requests.get(
                "http://127.0.0.1:8000/predict-soil",
                params=st.session_state.weather
            ).json()

            st.session_state.soil = soil

            crop = requests.get(
                "http://127.0.0.1:8000/predict-crop",
                params={
                    **soil,
                    **st.session_state.weather
                }
            ).json()

            st.success(f"Best Crop: {crop['prediction']}")

            for i, c in enumerate(crop["top3"], 1):
                st.write(f"{i}. {c['crop']} ({c['confidence']})")

        except Exception as e:
            st.error("Auto failed")
            st.code(str(e))

    # Reset
    if col3.button("Reset"):
        st.session_state.weather = {"temp": 25, "humidity": 60, "rain": 500}
        st.session_state.soil = {"N": 50, "P": 50, "K": 50, "ph": 6.5}

    # Weather Inputs
    st.subheader("Weather Inputs")

    temp = st.slider("Temperature", 10, 45, st.session_state.weather["temp"])
    humidity = st.slider("Humidity", 10, 100, st.session_state.weather["humidity"])
    rain = st.slider("Rainfall", 0, 3000, st.session_state.weather["rain"])

    # Soil Button
    if st.button("Find Soil Values"):
        try:
            soil = requests.get(
                "http://127.0.0.1:8000/predict-soil",
                params={"temp": temp, "humidity": humidity, "rain": rain}
            ).json()

            st.session_state.soil = soil
            st.success("Soil updated")

        except:
            st.error("Soil API failed")

    # Soil Inputs
    st.subheader("Soil Inputs")

    N = st.number_input("Nitrogen", 0, 150, int(st.session_state.soil["N"]))
    P = st.number_input("Phosphorus", 0, 150, int(st.session_state.soil["P"]))
    K = st.number_input("Potassium", 0, 150, int(st.session_state.soil["K"]))
    ph = st.slider("pH", 3.5, 9.0, float(st.session_state.soil["ph"]))

    # Predict
    if st.button("Predict Crop"):
        try:
            data = requests.get(
                "http://127.0.0.1:8000/predict-crop",
                params={
                    "N": N,
                    "P": P,
                    "K": K,
                    "temp": temp,
                    "humidity": humidity,
                    "ph": ph,
                    "rain": rain
                }
            ).json()

            st.success(f"Best Crop: {data['prediction']}")

            for i, c in enumerate(data["top3"], 1):
                st.write(f"{i}. {c['crop']} ({c['confidence']})")

        except Exception as e:
            st.error("Server error")
            st.code(str(e))


# ==========================
# CROP ANALYSIS PAGE
# ==========================
elif page == "Crop Analysis":

    st.title("Crop Analysis")

    df = pd.read_csv("data/crop_full_data.csv")

    st.sidebar.subheader("Filter")
    crop = st.sidebar.selectbox(
        "Select Crop",
        ["All"] + sorted(df["label"].unique())
    )

    if crop != "All":
        df = df[df["label"] == crop]

    st.metric("Total Records", len(df))

    st.dataframe(df.head(), use_container_width=True)

    # Scatter Plot
    st.subheader("Temperature vs Rainfall")

    fig, ax = plt.subplots()

    for c in df["label"].unique():
        sub = df[df["label"] == c]
        ax.scatter(sub["temperature"], sub["rainfall"], label=c)

    ax.set_xlabel("Temperature")
    ax.set_ylabel("Rainfall")
    ax.legend()

    st.pyplot(fig)