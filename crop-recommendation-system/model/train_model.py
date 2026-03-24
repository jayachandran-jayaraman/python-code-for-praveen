import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("data/crop_full_data.csv")

X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]
y = df["label"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

joblib.dump(model, "model/crop_model.pkl")

print("Crop model trained")