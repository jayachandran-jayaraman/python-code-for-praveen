from fastapi import FastAPI, HTTPException
import joblib

app = FastAPI()

# Load models
crop_model = joblib.load("model/crop_model.pkl")
soil_model = joblib.load("model/soil_model.pkl")


# ==========================
# Soil Prediction API
# ==========================
@app.get("/predict-soil")
def predict_soil(temp: float, humidity: float, rain: float):
    try:
        pred = soil_model.predict([[temp, humidity, rain]])[0]

        return {
            "N": round(pred[0], 2),
            "P": round(pred[1], 2),
            "K": round(pred[2], 2),
            "ph": round(pred[3], 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================
# Crop Prediction API
# ==========================
@app.get("/predict-crop")
def predict_crop(N: float, P: float, K: float, temp: float, humidity: float, ph: float, rain: float):
    try:
        pred = crop_model.predict([[N, P, K, temp, humidity, ph, rain]])[0]

        probs = crop_model.predict_proba([[N, P, K, temp, humidity, ph, rain]])[0]
        classes = crop_model.classes_

        top3 = sorted(
            [{"crop": c, "confidence": round(p, 3)} for c, p in zip(classes, probs)],
            key=lambda x: x["confidence"],
            reverse=True
        )[:3]

        return {
            "prediction": pred,
            "top3": top3
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))