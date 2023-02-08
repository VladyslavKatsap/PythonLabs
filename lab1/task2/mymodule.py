import requests

APPID = "a2087aa974bd561a2f044deb771ba6f9"
URL_BASE = "https://api.openweathermap.org/data/2.5/"


def current_weather(q: str = "Chicago", appid: str = APPID) -> dict:
    return requests.get(URL_BASE + "weather", params=locals()).json()