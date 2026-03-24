import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("data/crop_full_data.csv")

X = df[["temperature", "humidity", "rainfall"]]
y = df[["N", "P", "K", "ph"]]

model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)

joblib.dump(model, "model/soil_model.pkl")

print("Soil model trained")