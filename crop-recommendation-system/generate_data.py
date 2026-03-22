import pandas as pd
import random

data = []

crops = {
    "rice": (20, 35, 80, 90, 6.0, 7.5, 200, 300),
    "wheat": (10, 25, 50, 70, 6.0, 7.0, 300, 500),
    "maize": (18, 30, 70, 85, 6.0, 7.5, 500, 700),
    "barley": (10, 20, 40, 60, 6.0, 7.0, 250, 350),

    "sugarcane": (25, 40, 80, 95, 6.5, 7.5, 1000, 1600),
    "cotton": (25, 35, 60, 75, 6.0, 7.0, 700, 900),

    "chickpea": (15, 30, 40, 60, 6.0, 7.5, 300, 600),
    "lentil": (10, 25, 40, 60, 6.0, 7.0, 250, 500),

    "mustard": (10, 25, 50, 70, 6.0, 7.5, 300, 500),
    "groundnut": (20, 35, 60, 80, 6.0, 7.0, 500, 800),

    "tomato": (18, 30, 60, 80, 6.0, 7.5, 400, 700),
    "potato": (10, 25, 60, 80, 5.5, 6.5, 300, 600),

    "banana": (25, 35, 75, 90, 6.0, 7.5, 1000, 2000),
    "watermelon": (22, 35, 60, 80, 6.0, 7.5, 400, 700)
}

for crop, (tmin, tmax, hmin, hmax, phmin, phmax, rmin, rmax) in crops.items():
    for _ in range(20):  # 👈 20 rows each crop
        row = {
            "N": random.randint(40, 120),
            "P": random.randint(20, 80),
            "K": random.randint(20, 70),
            "temperature": round(random.uniform(tmin, tmax), 2),
            "humidity": round(random.uniform(hmin, hmax), 2),
            "ph": round(random.uniform(phmin, phmax), 2),
            "rainfall": round(random.uniform(rmin, rmax), 2),
            "label": crop
        }
        data.append(row)

df = pd.DataFrame(data)
df.to_csv("data/crop_full_data.csv", index=False)

print("✅ Dataset generated with multiple crops (20 rows each)")