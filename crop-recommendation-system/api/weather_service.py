import requests
from config import WEATHER_API_URL, SEASON_DAYS

def get_current_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "precipitation",
        "current_weather": True
    }

    data = requests.get(WEATHER_API_URL, params=params).json()

    temperature = data["current_weather"]["temperature"]

    hourly_rain = data.get("hourly", {}).get("precipitation", [])
    daily_rain = sum(hourly_rain[:24]) if hourly_rain else 0

    seasonal_rainfall = daily_rain * SEASON_DAYS

    return temperature, daily_rain, seasonal_rainfall
