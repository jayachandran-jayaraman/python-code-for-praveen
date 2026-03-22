import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load data
df = pd.read_csv("data/crop_full_data.csv")

X = df.drop("label", axis=1)
y = df["label"]

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Save model
with open("model/crop_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained & saved")