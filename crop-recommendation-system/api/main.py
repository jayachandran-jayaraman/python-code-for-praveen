from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

try:
    crops = pd.read_csv("data/crop_requirements.csv")
except Exception as e:
    raise RuntimeError(f"CSV Load Error: {e}")

@app.get("/recommend")
def recommend(temp: float, rain: float, season: str):
    try:
        season = season.lower()
        results = []

        for _, row in crops.iterrows():
            score = 0.0

            # Temperature
            if row["min_temp"] <= temp <= row["max_temp"]:
                score += 0.4

            # Rainfall
            if row["min_rain"] <= rain <= row["max_rain"]:
                score += 0.4

            # Season
            if row["season"].lower() == season:
                score += 0.2

            results.append({
                "crop": row["crop"],
                "score": round(score, 3)
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)
        return results[:3]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
