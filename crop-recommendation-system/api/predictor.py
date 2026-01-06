import pandas as pd

def recommend_top_crops(temp, rain):
    data = pd.read_csv("data/crop_requirements.csv")

    data["temp_score"] = 1 - abs(
        ((data["min_temp"] + data["max_temp"]) / 2) - temp
    ) / 50

    data["rain_score"] = 1 - abs(
        ((data["min_rain"] + data["max_rain"]) / 2) - rain
    ) / 3000

    data["total_score"] = (data["temp_score"] + data["rain_score"]) / 2
    data["confidence"] = (data["total_score"] * 100).round(2)

    top3 = data.sort_values("confidence", ascending=False).head(3)

    return top3[["crop", "confidence"]]
