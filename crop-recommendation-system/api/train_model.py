import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("data/crop_requirements.csv")

X = data[["min_temp","max_temp","min_rain","max_rain"]]
y = data["crop"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

joblib.dump(model, "model/rf_crop_model.pkl")
print("Model trained & saved")
