"""
Basic Weather App (Beginner Tier)
------------------------------------
Fetches and displays current weather for a user-specified city using
the OpenWeatherMap API.

Setup:
    1. Get a free API key from https://openweathermap.org/api
    2. Set it as an environment variable named OPENWEATHERMAP_API_KEY
       OR paste it directly into the API_KEY variable below (not recommended
       for anything you commit publicly).

Run:
    python weather_app.py
"""

import os
import sys
import requests

API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_city() -> str:
    while True:
        city = input("Enter a city name (or ZIP,country e.g. 10001,us): ").strip()
        if not city:
            print("  ⚠ City name cannot be empty. Try again.")
            continue
        return city


def fetch_weather(city: str, api_key: str) -> dict | None:
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",  # gives Celsius directly; we derive Fahrenheit ourselves
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.exceptions.Timeout:
        print("  ⚠ Network timeout. Check your internet connection and try again.")
        return None
    except requests.exceptions.ConnectionError:
        print("  ⚠ Could not connect to the weather service. Check your internet connection.")
        return None

    if response.status_code == 401:
        print("  ⚠ Invalid API key. Double-check your OPENWEATHERMAP_API_KEY.")
        return None
    if response.status_code == 404:
        print(f"  ⚠ City '{city}' not found. Check the spelling and try again.")
        return None
    if response.status_code != 200:
        print(f"  ⚠ Unexpected error from weather service (status {response.status_code}).")
        return None

    return response.json()


def display_weather(data: dict):
    city_name = data.get("name", "Unknown")
    country = data.get("sys", {}).get("country", "")
    temp_c = data["main"]["temp"]
    temp_f = temp_c * 9 / 5 + 32
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"].title()
    wind_speed = data["wind"]["speed"]

    print("\n" + "-" * 45)
    print(f"Weather in {city_name}, {country}")
    print("-" * 45)
    print(f"Condition   : {description}")
    print(f"Temperature : {temp_c:.1f}°C  /  {temp_f:.1f}°F")
    print(f"Humidity    : {humidity}%")
    print(f"Wind Speed  : {wind_speed} m/s")
    print("-" * 45)


def main():
    print("=" * 45)
    print("            BASIC WEATHER APP")
    print("=" * 45)

    if not API_KEY:
        print(
            "\n⚠ No API key found.\n"
            "Set the OPENWEATHERMAP_API_KEY environment variable before running,\n"
            "e.g. (macOS/Linux): export OPENWEATHERMAP_API_KEY=your_key_here\n"
            "     (Windows PS)  : setx OPENWEATHERMAP_API_KEY \"your_key_here\"\n"
        )
        sys.exit(1)

    while True:
        city = get_city()
        data = fetch_weather(city, API_KEY)
        if data:
            display_weather(data)

        again = input("\nCheck another city? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()
