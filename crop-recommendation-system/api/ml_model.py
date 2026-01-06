import joblib
import pandas as pd

model = joblib.load("model/rf_crop_model.pkl")

def ml_predict(temp, rain):
    X = pd.DataFrame([[temp, rain]], columns=["temperature", "rainfall"])
    probs = model.predict_proba(X)[0]
    return probs
