import requests
from bs4 import BeautifulSoup

def get_city():
    city = input("Please enter the name of the city: ")
    if city.lower() in ["moscow", "st. petersburg", "kazan", "novosibirsk", "yekaterinburg"]:
        print("Country 404")
    else:
        print("City is: " + city)


def get_weather(city):
    url = 'https://www.weather-forecast.com/locations/' + city + '/forecasts/latest'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    weather_data = soup.find_all('span', class_='b-forecast__table-description-title')
    weather = weather_data[0].text
    print(weather)