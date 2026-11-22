
import requests
import time
from datetime import datetime

API_KEY = "d21d7e59e85d1149d322a363e50f86e6"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

        # Location information
        city_name = data["name"]
        country = data["sys"]["country"]

        # Weather information
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        weather = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        wind_direction = data["wind"].get("deg", "N/A")

        clouds = data["clouds"]["all"]
        visibility = data.get("visibility", 0) / 1000

        # Convert timestamps using location timezone
        timezone = data["timezone"]

        def convert_time(timestamp):
            from datetime import timedelta, timezone as tz

            local_tz = tz(timedelta(seconds=timezone))
            return datetime.fromtimestamp(
                timestamp, tz=local_tz
            ).strftime("%I:%M %p")

        sunrise = convert_time(data["sys"]["sunrise"])
        sunset = convert_time(data["sys"]["sunset"])

        last_updated = convert_time(data["dt"])

        # Display report
        print("\n" + "=" * 45)
        print("          LIVE WEATHER REPORT")
        print("=" * 45)

        print(f"Location       : {city_name}, {country}")
        print(f"Temperature    : {temperature} °C")
        print(f"Feels Like     : {feels_like} °C")
        print(f"Condition      : {weather.title()}")
        print(f"Humidity       : {humidity}%")
        print(f"Pressure       : {pressure} hPa")
        print(f"Wind Speed     : {wind_speed} m/s")
        print(f"Wind Direction : {wind_direction}°")
        print(f"Cloud Coverage : {clouds}%")
        print(f"Visibility     : {visibility} km")
        print(f"Sunrise        : {sunrise}")
        print(f"Sunset         : {sunset}")
        print(f"Data Updated   : {last_updated}")

        print("=" * 45)

    except requests.exceptions.HTTPError as error:
        if response.status_code == 404:
            print("City not found.")
        elif response.status_code == 401:
            print("Invalid API key.")
        elif response.status_code == 429:
            print("API request limit reached.")
        else:
            print("HTTP Error:", error)

    except requests.exceptions.RequestException as error:
        print("Network Error:", error)

    except (KeyError, ValueError, TypeError) as error:
        print("Unexpected API response:", error)


# Main application
if __name__ == "__main__":

    city = input("Enter city name: ").strip()

    if not city:
        print("Please enter a valid city.")
    else:
        while True:

            print("\nFetching latest available weather data...")

            get_weather(city)

            print("\nNext refresh in 10 minutes.")
            print("Press CTRL + C to stop.")

            try:
                time.sleep(600)

            except KeyboardInterrupt:
                print("\nWeather application stopped.")
                break
