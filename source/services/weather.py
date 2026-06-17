import requests

BASE_URL = "https://api.responsible-nlp.net/weather.php"

def get_weather_forecast(place: str):
    try:
        response = requests.post(
            BASE_URL,
            data={"place": place}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"API request failed: {e}")


if __name__ == "__main__":
    result = get_weather_forecast("Marburg")
    print(result)
