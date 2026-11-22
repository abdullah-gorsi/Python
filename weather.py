import requests

API_KEY = "d21d7e59e85d1149d322a363e50f86e6"

def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code == 200:
            print("\n========== WEATHER REPORT ==========")
            print(f"City        : {data['name']}")
            print(f"Temperature : {data['main']['temp']} °C")
            print(f"Feels Like  : {data['main']['feels_like']} °C")
            print(f"Humidity    : {data['main']['humidity']}%")
            print(f"Pressure    : {data['main']['pressure']} hPa")
            print(f"Weather     : {data['weather'][0]['description'].title()}")
            print(f"Wind Speed  : {data['wind']['speed']} m/s")
            print("====================================")

        else:
            print("Error:", data.get("message", "Unable to fetch weather"))

    except requests.exceptions.RequestException as error:
        print("Connection error:", error)


# Main Program
print("Welcome to Python Weather App!")

city = input("Enter city name: ")

get_weather(city)
