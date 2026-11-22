
import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5"
GEO_URL = "https://api.openweathermap.org/geo/1.0"


class WeatherAPI:

    def __init__(self):
        if not API_KEY:
            raise ValueError(
                "OPENWEATHER_API_KEY is missing. "
                "Check your .env file."
            )

        self.session = requests.Session()

    def request(self, url, params):
        params["appid"] = API_KEY

        response = self.session.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()
        return response.json()

    # Convert city name into coordinates
    def get_coordinates(self, city):

        data = self.request(
            f"{GEO_URL}/direct",
            {
                "q": city,
                "limit": 1
            }
        )

        if not data:
            raise ValueError("City not found.")

        return {
            "name": data[0]["name"],
            "country": data[0]["country"],
            "lat": data[0]["lat"],
            "lon": data[0]["lon"]
        }

    # Current weather
    def get_current_weather(self, lat, lon):

        return self.request(
            f"{BASE_URL}/weather",
            {
                "lat": lat,
                "lon": lon,
                "units": "metric"
            }
        )

    # Five-day forecast (3-hour intervals)
    def get_forecast(self, lat, lon):

        return self.request(
            f"{BASE_URL}/forecast",
            {
                "lat": lat,
                "lon": lon,
                "units": "metric"
            }
        )

    # Air quality
    def get_air_quality(self, lat, lon):

        return self.request(
            f"{BASE_URL}/air_pollution",
            {
                "lat": lat,
                "lon": lon
            }
        )
