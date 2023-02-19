import telebot
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot("6116036028:AAFIceklU-Wwz0TSC_cq9wJbrZ8NS4K_D50")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Привіт, введіть номер автомобіля, марку автомобіля, модель, об'єм двигуна, розділивши їх комами. \nНаприклад: AA1234BB, BMW, X6, 3.0
""")
    bot.register_next_step_handler(msg, search_car)

def search_car(message):
    car_info = message.text.split(',')
    brand = car_info[1].strip()
    model = car_info[2].strip()
    url = f'https://auto.ria.com/uk/legkovie/{brand}/{model}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_ranges = soup.find_all('span', {'class': 'bold green size22'})
    if len(price_ranges) == 0:
        bot.reply_to(message, "На жаль, ми не змогли знайти інформацію про ціну на цей автомобіль.")
    else:
        price_range = price_ranges[0].text.strip()
        bot.reply_to(message, f"Діапазон цін на автомобіль {brand} {model}: {price_range}.")


bot.polling()