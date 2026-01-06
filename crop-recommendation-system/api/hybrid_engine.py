import pandas as pd

def hybrid_recommendation(temp, rain, soil, season, ml_probs):
    crops = pd.read_csv("data/crop_requirements.csv")
    crops["score"] = ml_probs

    for i, row in crops.iterrows():
        if row.min_temp <= temp <= row.max_temp:
            crops.at[i, "score"] += 0.2
        if row.min_rain <= rain <= row.max_rain:
            crops.at[i, "score"] += 0.3
        if row.season == season:
            crops.at[i, "score"] += 0.2

    return crops.sort_values("score", ascending=False).head(3)
