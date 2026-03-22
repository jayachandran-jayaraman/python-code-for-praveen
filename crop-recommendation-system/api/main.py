from fastapi import FastAPI, HTTPException
import pickle
import numpy as np

app = FastAPI()

# Load model
try:
    with open("model/crop_model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Model Load Error: {e}")


@app.get("/predict")
def predict(
    N: float,
    P: float,
    K: float,
    temperature: float,
    humidity: float,
    ph: float,
    rainfall: float
):
    try:
        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

        prediction = model.predict(input_data)[0]
        probs = model.predict_proba(input_data)[0]

        top3_idx = probs.argsort()[-3:][::-1]
        top3 = [
            {
                "crop": model.classes_[i],
                "confidence": round(float(probs[i]), 3)
            }
            for i in top3_idx
        ]

        return {
            "prediction": prediction,
            "top3": top3
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))