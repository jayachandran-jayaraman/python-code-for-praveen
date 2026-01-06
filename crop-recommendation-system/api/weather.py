import requests

def get_7day_rainfall(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "precipitation_sum",
        "forecast_days": 7
    }
    data = requests.get(url, params=params).json()
    return sum(data["daily"]["precipitation_sum"])
