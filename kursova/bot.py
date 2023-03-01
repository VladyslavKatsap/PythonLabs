import dp as dp
import telebot
import requests
from bs4 import BeautifulSoup
import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hlink, link
import os
from aiogram.dispatcher.filters import Text

bot = telebot.TeleBot("6116036028:AAFIceklU-Wwz0TSC_cq9wJbrZ8NS4K_D50")

strt = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
strt.row('Розмитнити авто!')
strt.one_time_keyboard = True

re = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
re.row('Так!')
re.one_time_keyboard = True

brands = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'Nissan', 'Jeep', 'GMC', 'Subaru', 'Lada', 'Hyundai', 'Kia', 'Mazda',
          'Dodge', 'BMW', 'Mercedes-Benz', 'Volkswagen', 'Lexus', 'Audi', 'Peugeot', 'Renault', 'Opel', 'Інший']

years = ['1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
         '2009', '2010', '2011', '2012',
         '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', 'Інший']

models = ['4Runner', 'Avalon', 'Camry', 'Corolla', 'Highlander', 'Land Cruiser', 'Prius', 'RAV4', 'Sienna', 'Tacoma',
          'Accord', 'Civic', 'CR-V', 'Fit', 'Odyssey', 'Passport', 'Pilot', 'Ridgeline', 'Insight', 'Clarity',
          'Bronco', 'Escape', 'Explorer', 'F-150', 'Fusion', 'Mustang', 'Ranger', 'Taurus', 'Transit', 'Edge',
          'Camaro', 'Corvette', 'Equinox', 'Silverado', 'Tahoe', 'Traverse', 'Volt', 'Malibu', 'Impala', 'Suburban',
          'Altima', 'Armada', 'Frontier', 'GT-R', 'Maxima', 'Murano', 'Pathfinder', 'Rogue', 'Sentra', 'Titan',
          'Cherokee', 'Compass', 'Gladiator', 'Grand Cherokee', 'Renegade', 'Wrangler', 'Commander', 'Liberty',
          'Patriot', 'Wagoneer',
          'Acadia', 'Canyon', 'Sierra', 'Terrain', 'Yukon', 'Savana', 'Envoy', 'Jimmy', 'Tracker', 'Suburban',
          'Ascent', 'Crosstrek', 'Forester', 'Impreza', 'Legacy', 'Outback', 'BRZ', 'WRX', 'Baja', 'Tribeca',
          'Vesta', 'Granta', 'Niva', 'XRAY', 'Priora', 'Largus', 'Kalina', 'Samara', '2107 ', '2106',
          'Accent', 'Elantra', 'Kona', 'Palisade', 'Santa Fe', 'Sonata', 'Tucson', 'Veloster', 'Ioniq', 'Venue',
          'Forte', 'Optima', 'Sorento', 'Soul', 'Sportage', 'Stinger', 'Cadenza', 'K5', 'Niro', 'Rio',
          'CX-5', 'CX-9', 'MAZDA3', 'MAZDA6', 'MX-5 Miata', 'RX-7', 'RX-8', 'CX-3', 'B-Series', 'MPV',
          'Challenger', 'Charger', 'Durango', 'Grand Caravan', 'Journey', 'Neon', 'Ram Van', 'Viper', 'Nitro',
          'Caliber',
          '3 Series', '5 Series', 'X5', '7 Series', 'M3', 'M5', 'X3', 'Z4', '6 Series', '4 Series',
          'C-Class', 'E-Class', 'S-Class', 'GLC-Class', 'G-Class', 'SL-Class', 'SLK-Class', 'M-Class', 'CLS-Class',
          'CL-Class',
          'Atlas', 'Beetle', 'Golf', 'Jetta', 'Passat', 'Tiguan', 'Touareg', 'Arteon', 'ID.4', 'Taos',
          'RX', 'NX', 'ES', 'IS', 'UX', 'LS', 'GX', 'RC', 'LC', 'CT',
          'A4', 'A3', 'Q5', 'Q7', 'A6', 'A5', 'Q3', 'A1', 'A7', 'TT',
          '208', '3008', '308', '508', '207', '206', '407', '307', '108',
          'Clio', 'Megane', 'Captur', 'Kadjar', 'Twingo', 'Scenic', 'Zoe', 'Koleos', 'Talisman', 'Espace',
          'Astra', 'Corsa', 'Insignia', 'Mokka', 'Zafira', 'Adam', 'Crossland X', 'Grandland X', 'Karl', 'Antara',
          'Інша модель']

engine_types = ['Бензиновий', 'Дизельний', 'Гібридний', 'Електричний', 'Інший']
engines = ['1.0', '1.2', '1.3', '1.4', '1.5', '1.6', '1.8', '1.9', '2.0', '2.2', '2.4', '2.5', '2.7', '2.8', '3.0',
           '3.5', '4.0', '4.6', '5.0', '6.2', '50 кВт', '75 кВт', '100 кВт', '125 кВт', '150 кВт', '175 кВт',
           '200 кВт', 'Інший']

prices = ['До 470 тис. грн.', 'До 720 тис. грн.', 'Понад 720 тис. грн.']


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привіт, це бот для розмитнення автомобілів.\nНатисніть кнопку "Розмитнити авто!", та слідуйте за вказівками.',
                     reply_markup=strt)


@bot.message_handler(commands=['reset'])
def reset_message(message):
    bot.send_message(message.chat.id, 'Давайте ще раз', reply_markup=re)
    number = ""  # номер авто
    brand = ""  # бренд авто
    model = ""  # модель бренду авто
    year = ""  # рік випуску
    engine_type = ""  # тип палива
    engine = ""  # об'єм двигуна
    price = ""  # ціна покупки
    return number, brand, model, year, engine_type, engine, price
    brand(message)


@bot.message_handler(content_types=["text"])
def brand(message):
    mark = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text="Toyota", callback_data="Toyota")
    button2 = telebot.types.InlineKeyboardButton(text="Honda", callback_data="Honda")
    button3 = telebot.types.InlineKeyboardButton(text="Ford", callback_data="Ford")
    button4 = telebot.types.InlineKeyboardButton(text="Chevrolet", callback_data="Chevrolet")
    button5 = telebot.types.InlineKeyboardButton(text="Nissan", callback_data="Nissan")
    button6 = telebot.types.InlineKeyboardButton(text="Jeep", callback_data="Jeep")
    button7 = telebot.types.InlineKeyboardButton(text="GMC", callback_data="GMC")
    button8 = telebot.types.InlineKeyboardButton(text="Subaru", callback_data="Subaru")
    button9 = telebot.types.InlineKeyboardButton(text="Lada", callback_data="Lada")
    button10 = telebot.types.InlineKeyboardButton(text="Hyundai", callback_data="Hyundai")
    button11 = telebot.types.InlineKeyboardButton(text="Kia", callback_data="Kia")
    button12 = telebot.types.InlineKeyboardButton(text="Mazda", callback_data="Mazda")
    button13 = telebot.types.InlineKeyboardButton(text="Dodge", callback_data="Dodge")
    button14 = telebot.types.InlineKeyboardButton(text="BMW", callback_data="BMW")
    button15 = telebot.types.InlineKeyboardButton(text="Mercedes-Benz", callback_data="Mercedes-Benz")
    button16 = telebot.types.InlineKeyboardButton(text="Volkswagen", callback_data="Volkswagen")
    button17 = telebot.types.InlineKeyboardButton(text="Lexus", callback_data="Lexus")
    button18 = telebot.types.InlineKeyboardButton(text="Audi", callback_data="Audi")
    button19 = telebot.types.InlineKeyboardButton(text="Peugeot", callback_data="Peugeot")
    button20 = telebot.types.InlineKeyboardButton(text="Renault", callback_data="Renault")
    button21 = telebot.types.InlineKeyboardButton(text="Opel", callback_data="Opel")
    mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
             button12, button13, button14, button15, button16, button17, button18, button19, button20, button21)
    bot.send_message(message.chat.id, 'Оберіть бренд автомобіля', reply_markup=mark)


@bot.callback_query_handler(func=lambda call: call.data in brands)
def query_brand(call):
    bot.answer_callback_query(callback_query_id=call.id)
    global br
    br = call.data
    bot.send_message(call.message.chat.id, 'Обраний бренд: ' + br)
    print(br)
    model(call.message)


@bot.message_handler(content_types=["text"])
def model(message):
    if br == "Toyota":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="4Runner", callback_data="4Runner")
        button2 = telebot.types.InlineKeyboardButton(text="Avalon", callback_data="Avalon")
        button3 = telebot.types.InlineKeyboardButton(text="Camry", callback_data="Camry")
        button4 = telebot.types.InlineKeyboardButton(text="Corolla", callback_data="Corolla")
        button5 = telebot.types.InlineKeyboardButton(text="Highlander", callback_data="Highlander")
        button6 = telebot.types.InlineKeyboardButton(text="Land Cruiser", callback_data="Land Cruiser")
        button7 = telebot.types.InlineKeyboardButton(text="Prius", callback_data="Prius")
        button8 = telebot.types.InlineKeyboardButton(text="RAV4", callback_data="RAV4")
        button9 = telebot.types.InlineKeyboardButton(text="Sienna", callback_data="Sienna")
        button10 = telebot.types.InlineKeyboardButton(text="Tacoma", callback_data="Tacoma")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)

    elif br == "Honda":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Accord", callback_data="Accord")
        button2 = telebot.types.InlineKeyboardButton(text="Civic", callback_data="Civic")
        button3 = telebot.types.InlineKeyboardButton(text="CR-V", callback_data="CR-V")
        button4 = telebot.types.InlineKeyboardButton(text="Fit", callback_data="Fit")
        button5 = telebot.types.InlineKeyboardButton(text="Odyssey", callback_data="Odyssey")
        button6 = telebot.types.InlineKeyboardButton(text="Passport", callback_data="Passport")
        button7 = telebot.types.InlineKeyboardButton(text="Pilot", callback_data="Pilot")
        button8 = telebot.types.InlineKeyboardButton(text="Ridgeline", callback_data="Ridgeline")
        button9 = telebot.types.InlineKeyboardButton(text="Insight", callback_data="Insight")
        button10 = telebot.types.InlineKeyboardButton(text="Clarity", callback_data="Clarity")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)


    elif br == "Ford":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Bronco", callback_data="Bronco")
        button2 = telebot.types.InlineKeyboardButton(text="Escape", callback_data="Escape")
        button3 = telebot.types.InlineKeyboardButton(text="Explorer", callback_data="Explorer")
        button4 = telebot.types.InlineKeyboardButton(text="F-150", callback_data="F-150")
        button5 = telebot.types.InlineKeyboardButton(text="Fusion", callback_data="Fusion")
        button6 = telebot.types.InlineKeyboardButton(text="Mustang", callback_data="Mustang")
        button7 = telebot.types.InlineKeyboardButton(text="Ranger", callback_data="Ranger")
        button8 = telebot.types.InlineKeyboardButton(text="Taurus", callback_data="Taurus")
        button9 = telebot.types.InlineKeyboardButton(text="Transit", callback_data="Transit")
        button10 = telebot.types.InlineKeyboardButton(text="Edge", callback_data="Edge")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)


    elif br == "Chevrolet":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Camaro", callback_data="Camaro")
        button2 = telebot.types.InlineKeyboardButton(text="Corvette", callback_data="Corvette")
        button3 = telebot.types.InlineKeyboardButton(text="Equinox", callback_data="Equinox")
        button4 = telebot.types.InlineKeyboardButton(text="Silverado", callback_data="Silverado")
        button5 = telebot.types.InlineKeyboardButton(text="Tahoe", callback_data="Tahoe")
        button6 = telebot.types.InlineKeyboardButton(text="Traverse", callback_data="Traverse")
        button7 = telebot.types.InlineKeyboardButton(text="Volt", callback_data="Volt")
        button8 = telebot.types.InlineKeyboardButton(text="Malibu", callback_data="Malibu")
        button9 = telebot.types.InlineKeyboardButton(text="Impala", callback_data="Impala")
        button10 = telebot.types.InlineKeyboardButton(text="Suburban", callback_data="Suburban")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)


    elif br == "Nissan":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Altima", callback_data="Altima")
        button2 = telebot.types.InlineKeyboardButton(text="Armada", callback_data="Armada")
        button3 = telebot.types.InlineKeyboardButton(text="Frontier", callback_data="Frontier")
        button4 = telebot.types.InlineKeyboardButton(text="GT-R", callback_data="GT-R")
        button5 = telebot.types.InlineKeyboardButton(text="Maxima", callback_data="Maxima")
        button6 = telebot.types.InlineKeyboardButton(text="Murano", callback_data="Murano")
        button7 = telebot.types.InlineKeyboardButton(text="Pathfinder", callback_data="Pathfinder")
        button8 = telebot.types.InlineKeyboardButton(text="Rogue", callback_data="Rogue")
        button9 = telebot.types.InlineKeyboardButton(text="Sentra", callback_data="Sentra")
        button10 = telebot.types.InlineKeyboardButton(text="Titan", callback_data="Titan")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)

    elif br == "Jeep":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Cherokee", callback_data="Cherokee")
        button2 = telebot.types.InlineKeyboardButton(text="Compass", callback_data="Compass")
        button3 = telebot.types.InlineKeyboardButton(text="Gladiator", callback_data="Gladiator")
        button4 = telebot.types.InlineKeyboardButton(text="Grand Cherokee", callback_data="Grand Cherokee")
        button5 = telebot.types.InlineKeyboardButton(text="Renegade", callback_data="Renegade")
        button6 = telebot.types.InlineKeyboardButton(text="Wrangler", callback_data="Wrangler")
        button7 = telebot.types.InlineKeyboardButton(text="Commander", callback_data="Commander")
        button8 = telebot.types.InlineKeyboardButton(text="Liberty", callback_data="Liberty")
        button9 = telebot.types.InlineKeyboardButton(text="Patriot", callback_data="Patriot")
        button10 = telebot.types.InlineKeyboardButton(text="Wagoneer", callback_data="Wagoneer")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)



    elif br == "GMC":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Acadia", callback_data="Acadia")
        button2 = telebot.types.InlineKeyboardButton(text="Canyon", callback_data="Canyon")
        button3 = telebot.types.InlineKeyboardButton(text="Sierra", callback_data="Sierra")
        button4 = telebot.types.InlineKeyboardButton(text="Terrain", callback_data="Terrain")
        button5 = telebot.types.InlineKeyboardButton(text="Yukon", callback_data="Yukon")
        button6 = telebot.types.InlineKeyboardButton(text="Savana", callback_data="Savana")
        button7 = telebot.types.InlineKeyboardButton(text="Envoy", callback_data="Envoy")
        button8 = telebot.types.InlineKeyboardButton(text="Jimmy", callback_data="Jimmy")
        button9 = telebot.types.InlineKeyboardButton(text="Tracker", callback_data="Tracker")
        button10 = telebot.types.InlineKeyboardButton(text="Suburban", callback_data="Suburban")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)

    elif br == "Subaru":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Ascent", callback_data="Ascent")
        button2 = telebot.types.InlineKeyboardButton(text="Crosstrek", callback_data="Crosstrek")
        button3 = telebot.types.InlineKeyboardButton(text="Forester", callback_data="Forester")
        button4 = telebot.types.InlineKeyboardButton(text="Impreza", callback_data="Impreza")
        button5 = telebot.types.InlineKeyboardButton(text="Legacy", callback_data="Legacy")
        button6 = telebot.types.InlineKeyboardButton(text="Outback", callback_data="Outback")
        button7 = telebot.types.InlineKeyboardButton(text="BRZ", callback_data="BRZ")
        button8 = telebot.types.InlineKeyboardButton(text="WRX", callback_data="WRX")
        button9 = telebot.types.InlineKeyboardButton(text="Baja", callback_data="Baja")
        button10 = telebot.types.InlineKeyboardButton(text="Tribeca", callback_data="Tribeca")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)

    elif br == "Lada":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Vesta", callback_data="Vesta")
        button2 = telebot.types.InlineKeyboardButton(text="Granta", callback_data="Granta")
        button3 = telebot.types.InlineKeyboardButton(text="Niva", callback_data="Niva")
        button4 = telebot.types.InlineKeyboardButton(text="XRAY", callback_data="XRAY")
        button5 = telebot.types.InlineKeyboardButton(text="Priora", callback_data="Priora")
        button6 = telebot.types.InlineKeyboardButton(text="Largus", callback_data="Largus")
        button7 = telebot.types.InlineKeyboardButton(text="Kalina", callback_data="Kalina")
        button8 = telebot.types.InlineKeyboardButton(text="Samara", callback_data="Samara")
        button9 = telebot.types.InlineKeyboardButton(text="2107", callback_data="2107")
        button10 = telebot.types.InlineKeyboardButton(text="2106", callback_data="2106")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)


    elif br == "Hyundai":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Accent", callback_data="Accent")
        button2 = telebot.types.InlineKeyboardButton(text="Elantra", callback_data="Elantra")
        button3 = telebot.types.InlineKeyboardButton(text="Kona", callback_data="Kona")
        button4 = telebot.types.InlineKeyboardButton(text="Palisade", callback_data="Palisade")
        button5 = telebot.types.InlineKeyboardButton(text="Santa Fe", callback_data="Santa Fe")
        button6 = telebot.types.InlineKeyboardButton(text="Sonata", callback_data="Sonata")
        button7 = telebot.types.InlineKeyboardButton(text="Tucson", callback_data="Tucson")
        button8 = telebot.types.InlineKeyboardButton(text="Veloster", callback_data="Veloster")
        button9 = telebot.types.InlineKeyboardButton(text="Ioniq", callback_data="Ioniq")
        button10 = telebot.types.InlineKeyboardButton(text="Venue", callback_data="Venue")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)

    elif br == "Kia":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Forte", callback_data="Forte")
        button2 = telebot.types.InlineKeyboardButton(text="Optima", callback_data="Optima")
        button3 = telebot.types.InlineKeyboardButton(text="Sorento", callback_data="Sorento")
        button4 = telebot.types.InlineKeyboardButton(text="Soul", callback_data="Soul")
        button5 = telebot.types.InlineKeyboardButton(text="Sportage", callback_data="Sportage")
        button6 = telebot.types.InlineKeyboardButton(text="Stinger", callback_data="Stinger")
        button7 = telebot.types.InlineKeyboardButton(text="Cadenza", callback_data="Cadenza")
        button8 = telebot.types.InlineKeyboardButton(text="K5", callback_data="K5")
        button9 = telebot.types.InlineKeyboardButton(text="Niro", callback_data="Niro")
        button10 = telebot.types.InlineKeyboardButton(text="Rio", callback_data="Rio")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)

    elif br == "Mazda":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="CX-5", callback_data="CX-5")
        button2 = telebot.types.InlineKeyboardButton(text="CX-9", callback_data="CX-9")
        button3 = telebot.types.InlineKeyboardButton(text="MAZDA3", callback_data="MAZDA3")
        button4 = telebot.types.InlineKeyboardButton(text="MAZDA6", callback_data="MAZDA6")
        button5 = telebot.types.InlineKeyboardButton(text="MX-5 Miata", callback_data="MX-5 Miata")
        button6 = telebot.types.InlineKeyboardButton(text="RX-7", callback_data="RX-7")
        button7 = telebot.types.InlineKeyboardButton(text="RX-8", callback_data="RX-8")
        button8 = telebot.types.InlineKeyboardButton(text="CX-3", callback_data="CX-3")
        button9 = telebot.types.InlineKeyboardButton(text="B-Series", callback_data="B-Series")
        button10 = telebot.types.InlineKeyboardButton(text="MPV", callback_data="MPV")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)


    elif br == "Dodge":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Challenger", callback_data="Challenger")
        button2 = telebot.types.InlineKeyboardButton(text="Charger", callback_data="Charger")
        button3 = telebot.types.InlineKeyboardButton(text="Durango", callback_data="Durango")
        button4 = telebot.types.InlineKeyboardButton(text="Grand Caravan", callback_data="Grand Caravan")
        button5 = telebot.types.InlineKeyboardButton(text="Journey", callback_data="Journey")
        button6 = telebot.types.InlineKeyboardButton(text="Neon", callback_data="Neon")
        button7 = telebot.types.InlineKeyboardButton(text="Ram Van", callback_data="Ram Van")
        button8 = telebot.types.InlineKeyboardButton(text="Viper", callback_data="Viper")
        button9 = telebot.types.InlineKeyboardButton(text="Nitro", callback_data="Nitro")
        button10 = telebot.types.InlineKeyboardButton(text="Caliber", callback_data="Caliber")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)

    elif br == "BMW":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="3 Series", callback_data="3 Series")
        button2 = telebot.types.InlineKeyboardButton(text="5 Series", callback_data="5 Series")
        button3 = telebot.types.InlineKeyboardButton(text="X5", callback_data="X5")
        button4 = telebot.types.InlineKeyboardButton(text="7 Series", callback_data="7 Series")
        button5 = telebot.types.InlineKeyboardButton(text="M3", callback_data="M3")
        button6 = telebot.types.InlineKeyboardButton(text="M5", callback_data="M5")
        button7 = telebot.types.InlineKeyboardButton(text="X3", callback_data="X3")
        button8 = telebot.types.InlineKeyboardButton(text="Z4", callback_data="Z4")
        button9 = telebot.types.InlineKeyboardButton(text="6 Series", callback_data="6 Series")
        button10 = telebot.types.InlineKeyboardButton(text="4 Series", callback_data="4 Series")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)

    elif br == "Mercedes-Benz":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="C-Class", callback_data="C-Class")
        button2 = telebot.types.InlineKeyboardButton(text="E-Class", callback_data="E-Class")
        button3 = telebot.types.InlineKeyboardButton(text="S-Class", callback_data="S-Class")
        button4 = telebot.types.InlineKeyboardButton(text="GLC-Class", callback_data="GLC-Class")
        button5 = telebot.types.InlineKeyboardButton(text="G-Class", callback_data="G-Class")
        button6 = telebot.types.InlineKeyboardButton(text="SL-Class", callback_data="SL-Class")
        button7 = telebot.types.InlineKeyboardButton(text="SLK-Class", callback_data="SLK-Class")
        button8 = telebot.types.InlineKeyboardButton(text="M-Class", callback_data="M-Class")
        button9 = telebot.types.InlineKeyboardButton(text="CLS-Class", callback_data="CLS-Class")
        button10 = telebot.types.InlineKeyboardButton(text="CL-Class", callback_data="CL-Class")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)

    elif br == "Volkswagen":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Atlas", callback_data="Atlas")
        button2 = telebot.types.InlineKeyboardButton(text="Beetle", callback_data="Beetle")
        button3 = telebot.types.InlineKeyboardButton(text="Golf", callback_data="Golf")
        button4 = telebot.types.InlineKeyboardButton(text="Jetta", callback_data="Jetta")
        button5 = telebot.types.InlineKeyboardButton(text="Passat", callback_data="Passat")
        button6 = telebot.types.InlineKeyboardButton(text="Tiguan", callback_data="Tiguan")
        button7 = telebot.types.InlineKeyboardButton(text="Touareg", callback_data="Touareg")
        button8 = telebot.types.InlineKeyboardButton(text="Arteon", callback_data="Arteon")
        button9 = telebot.types.InlineKeyboardButton(text="ID.4", callback_data="ID.4")
        button10 = telebot.types.InlineKeyboardButton(text="Taos", callback_data="Taos")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)

    elif br == "Lexus":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="RX", callback_data="RX")
        button2 = telebot.types.InlineKeyboardButton(text="NX", callback_data="NX")
        button3 = telebot.types.InlineKeyboardButton(text="ES", callback_data="ES")
        button4 = telebot.types.InlineKeyboardButton(text="IS", callback_data="IS")
        button5 = telebot.types.InlineKeyboardButton(text="UX", callback_data="UX")
        button6 = telebot.types.InlineKeyboardButton(text="LS", callback_data="LS")
        button7 = telebot.types.InlineKeyboardButton(text="GX", callback_data="GX")
        button8 = telebot.types.InlineKeyboardButton(text="RC", callback_data="RC")
        button9 = telebot.types.InlineKeyboardButton(text="LC", callback_data="LC")
        button10 = telebot.types.InlineKeyboardButton(text="CT", callback_data="CT")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)

    elif br == "Audi":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="A4", callback_data="A4")
        button2 = telebot.types.InlineKeyboardButton(text="A3", callback_data="A3")
        button3 = telebot.types.InlineKeyboardButton(text="Q5", callback_data="Q5")
        button4 = telebot.types.InlineKeyboardButton(text="Q7", callback_data="Q7")
        button5 = telebot.types.InlineKeyboardButton(text="A6", callback_data="A6")
        button6 = telebot.types.InlineKeyboardButton(text="A5", callback_data="A5")
        button7 = telebot.types.InlineKeyboardButton(text="Q3", callback_data="Q3")
        button8 = telebot.types.InlineKeyboardButton(text="A1", callback_data="A1")
        button9 = telebot.types.InlineKeyboardButton(text="A7", callback_data="A7")
        button10 = telebot.types.InlineKeyboardButton(text="TT", callback_data="TT")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)

    elif br == "Peugeot":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="208", callback_data="208")
        button2 = telebot.types.InlineKeyboardButton(text="3008", callback_data="3008")
        button3 = telebot.types.InlineKeyboardButton(text="308", callback_data="308")
        button4 = telebot.types.InlineKeyboardButton(text="508", callback_data="508")
        button5 = telebot.types.InlineKeyboardButton(text="207", callback_data="207")
        button6 = telebot.types.InlineKeyboardButton(text="206", callback_data="206")
        button7 = telebot.types.InlineKeyboardButton(text="407", callback_data="407")
        button8 = telebot.types.InlineKeyboardButton(text="307", callback_data="307")
        button9 = telebot.types.InlineKeyboardButton(text="108", callback_data="108")
        button10 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button11 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button12 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)

    elif br == "Renault":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Clio", callback_data="Clio")
        button2 = telebot.types.InlineKeyboardButton(text="Megane", callback_data="Megane")
        button3 = telebot.types.InlineKeyboardButton(text="Captur", callback_data="Captur")
        button4 = telebot.types.InlineKeyboardButton(text="Kadjar", callback_data="Kadjar")
        button5 = telebot.types.InlineKeyboardButton(text="Twingo", callback_data="Twingo")
        button6 = telebot.types.InlineKeyboardButton(text="Scenic", callback_data="Scenic")
        button7 = telebot.types.InlineKeyboardButton(text="Zoe", callback_data="Zoe")
        button8 = telebot.types.InlineKeyboardButton(text="Koleos", callback_data="Koleos")
        button9 = telebot.types.InlineKeyboardButton(text="Talisman", callback_data="Talisman")
        button10 = telebot.types.InlineKeyboardButton(text="Espace", callback_data="Espace")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)

    elif br == "Opel":
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Astra", callback_data="Astra")
        button2 = telebot.types.InlineKeyboardButton(text="Corsa", callback_data="Corsa")
        button3 = telebot.types.InlineKeyboardButton(text="Insignia", callback_data="Insignia")
        button4 = telebot.types.InlineKeyboardButton(text="Mokka", callback_data="Mokka")
        button5 = telebot.types.InlineKeyboardButton(text="Zafira", callback_data="Zafira")
        button6 = telebot.types.InlineKeyboardButton(text="Adam", callback_data="Adam")
        button7 = telebot.types.InlineKeyboardButton(text="Crossland X", callback_data="Crossland X")
        button8 = telebot.types.InlineKeyboardButton(text="Grandland X", callback_data="Grandland X")
        button9 = telebot.types.InlineKeyboardButton(text="Karl", callback_data="Karl")
        button10 = telebot.types.InlineKeyboardButton(text="Antara", callback_data="Antara")
        button11 = telebot.types.InlineKeyboardButton(text="Інша модель", callback_data="Інша модель")
        button12 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button13 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13)
        bot.send_message(message.chat.id,
                         'Оберіть модель авто, або натисніть кнопку "Назад", щоб повернутися до попереднього кроку',
                         reply_markup=mark)


@bot.callback_query_handler(func=lambda call: call.data in models)
def query_mod(call):
    bot.answer_callback_query(callback_query_id=call.id)
    global mod
    mod = call.data
    if mod == 'Інша модель':
        bot.send_message(call.message.chat.id, 'Ця функція поки недоступна.')
    else:
        bot.send_message(call.message.chat.id, 'Обрана модель: ' + mod)
        print(mod)
        year(call.message)


@bot.message_handler(content_types=["text"])
def year(message):
    mark = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text="1995", callback_data="1995")
    button2 = telebot.types.InlineKeyboardButton(text="1996", callback_data="1996")
    button3 = telebot.types.InlineKeyboardButton(text="1997", callback_data="1997")
    button4 = telebot.types.InlineKeyboardButton(text="1998", callback_data="1998")
    button5 = telebot.types.InlineKeyboardButton(text="1999", callback_data="1999")
    button6 = telebot.types.InlineKeyboardButton(text="2000", callback_data="2000")
    button7 = telebot.types.InlineKeyboardButton(text="2001", callback_data="2001")
    button8 = telebot.types.InlineKeyboardButton(text="2002", callback_data="2002")
    button9 = telebot.types.InlineKeyboardButton(text="2003", callback_data="2003")
    button10 = telebot.types.InlineKeyboardButton(text="2004", callback_data="2004")
    button11 = telebot.types.InlineKeyboardButton(text="2005", callback_data="2005")
    button12 = telebot.types.InlineKeyboardButton(text="2006", callback_data="2006")
    button13 = telebot.types.InlineKeyboardButton(text="2007", callback_data="2007")
    button14 = telebot.types.InlineKeyboardButton(text="2008", callback_data="2008")
    button15 = telebot.types.InlineKeyboardButton(text="2009", callback_data="2009")
    button16 = telebot.types.InlineKeyboardButton(text="2010", callback_data="2010")
    button17 = telebot.types.InlineKeyboardButton(text="2011", callback_data="2011")
    button18 = telebot.types.InlineKeyboardButton(text="2012", callback_data="2012")
    button19 = telebot.types.InlineKeyboardButton(text="2013", callback_data="2013")
    button20 = telebot.types.InlineKeyboardButton(text="2014", callback_data="2014")
    button21 = telebot.types.InlineKeyboardButton(text="2015", callback_data="2015")
    button22 = telebot.types.InlineKeyboardButton(text="2016", callback_data="2016")
    button23 = telebot.types.InlineKeyboardButton(text="2017", callback_data="2017")
    button24 = telebot.types.InlineKeyboardButton(text="2018", callback_data="2018")
    button25 = telebot.types.InlineKeyboardButton(text="2019", callback_data="2019")
    button26 = telebot.types.InlineKeyboardButton(text="2020", callback_data="2020")
    button27 = telebot.types.InlineKeyboardButton(text="2021", callback_data="2021")
    button28 = telebot.types.InlineKeyboardButton(text="2022", callback_data="2022")
    button29 = telebot.types.InlineKeyboardButton(text="2023", callback_data="2023")
    button30 = telebot.types.InlineKeyboardButton(text="Інший", callback_data="Інший")
    button31 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
    button32 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
    mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
             button12, button13, button14, button15, button16, button17, button18, button19, button20, button21,
             button22, button23, button24, button25, button26, button27, button28, button29, button30, button31,
             button32)
    bot.send_message(message.chat.id, 'Оберіть рік випуску автомобіля', reply_markup=mark)


@bot.callback_query_handler(func=lambda call: call.data in years)
def query_year(call):
    bot.answer_callback_query(callback_query_id=call.id)
    global yer
    yer = call.data
    if yer == 'Інший':
        bot.send_message(call.message.chat.id, 'Ця функція поки недоступна.')
    else:
        bot.send_message(call.message.chat.id, 'Обраний рік випуску: ' + yer)
        print(yer)
        engine_type(call.message)


@bot.message_handler(content_types=["text"])
def engine_type(message):
    mark = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text="Бензиновий", callback_data="Бензиновий")
    button2 = telebot.types.InlineKeyboardButton(text="Дизельний", callback_data="Дизельний")
    button3 = telebot.types.InlineKeyboardButton(text="Гібридний", callback_data="Гібридний")
    button4 = telebot.types.InlineKeyboardButton(text="Електричний", callback_data="Електричний")
    button5 = telebot.types.InlineKeyboardButton(text="Інший", callback_data="Інший")
    button6 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
    button7 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
    mark.add(button1, button2, button3, button4, button5, button6, button7)
    bot.send_message(message.chat.id, 'Оберіть тип двигуна', reply_markup=mark)


@bot.callback_query_handler(func=lambda call: call.data in engine_types)
def query_enginetype(call):
    bot.answer_callback_query(callback_query_id=call.id)
    global ent
    ent = call.data
    if ent == 'Інший':
        bot.send_message(call.message.chat.id, 'Ця функція поки недоступна.')
    else:
        bot.send_message(call.message.chat.id, 'Обраний тип двигуна: ' + ent)
        print(ent)
        engine(call.message)


@bot.message_handler(content_types=["text"])
def engine(message):
    if ent == 'Бензиновий' or ent == 'Дизельний' or ent == 'Гібридний':
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="1.0", callback_data="1.0")
        button2 = telebot.types.InlineKeyboardButton(text="1.2", callback_data="1.2")
        button3 = telebot.types.InlineKeyboardButton(text="1.3", callback_data="1.3")
        button4 = telebot.types.InlineKeyboardButton(text="1.4", callback_data="1.4")
        button5 = telebot.types.InlineKeyboardButton(text="1.5", callback_data="1.5")
        button6 = telebot.types.InlineKeyboardButton(text="1.6", callback_data="1.6")
        button7 = telebot.types.InlineKeyboardButton(text="1.8", callback_data="1.8")
        button8 = telebot.types.InlineKeyboardButton(text="1.9", callback_data="1.9")
        button9 = telebot.types.InlineKeyboardButton(text="2.0", callback_data="2.0")
        button10 = telebot.types.InlineKeyboardButton(text="2.2", callback_data="2.2")
        button11 = telebot.types.InlineKeyboardButton(text="2.4", callback_data="2.4")
        button12 = telebot.types.InlineKeyboardButton(text="2.5", callback_data="2.5")
        button13 = telebot.types.InlineKeyboardButton(text="2.7", callback_data="2.7")
        button14 = telebot.types.InlineKeyboardButton(text="2.8", callback_data="2.8")
        button15 = telebot.types.InlineKeyboardButton(text="3.0", callback_data="3.0")
        button16 = telebot.types.InlineKeyboardButton(text="3.5", callback_data="3.5")
        button17 = telebot.types.InlineKeyboardButton(text="4.0", callback_data="4.0")
        button18 = telebot.types.InlineKeyboardButton(text="4.6", callback_data="4.6")
        button19 = telebot.types.InlineKeyboardButton(text="5.0", callback_data="5.0")
        button20 = telebot.types.InlineKeyboardButton(text="6.2", callback_data="6.2")
        button21 = telebot.types.InlineKeyboardButton(text="Інший", callback_data="Інший")
        button22 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button23 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
                 button12, button13, button14, button15, button16, button17, button18, button19, button20, button21,
                 button22, button23)
        bot.send_message(message.chat.id, "Оберіть об'єм двигуна", reply_markup=mark)

    elif ent == 'Електричний':
        mark = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="50_кВт", callback_data="50_кВт")
        button2 = telebot.types.InlineKeyboardButton(text="75 кВт", callback_data="75 кВт")
        button3 = telebot.types.InlineKeyboardButton(text="100 кВт", callback_data="100 кВт")
        button4 = telebot.types.InlineKeyboardButton(text="125 кВт", callback_data="125 кВт")
        button5 = telebot.types.InlineKeyboardButton(text="150 кВт", callback_data="150 кВт")
        button6 = telebot.types.InlineKeyboardButton(text="175 кВт", callback_data="175 кВт")
        button7 = telebot.types.InlineKeyboardButton(text="200 кВт", callback_data="200 кВт")
        button8 = telebot.types.InlineKeyboardButton(text="Інший", callback_data="Інший")
        button9 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
        button10 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
        mark.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10)
        bot.send_message(message.chat.id, "Оберіть потужність двигуна", reply_markup=mark)


@bot.callback_query_handler(func=lambda call: call.data in engines)
def query_enginetype(call):
    bot.answer_callback_query(callback_query_id=call.id)
    global eng
    eng = call.data
    if eng == 'Інший':
        bot.send_message(call.message.chat.id, 'Ця функція поки недоступна.')

    elif ent == 'Бензиновий' or 'Дизельний' or 'Гібридний':
        bot.send_message(call.message.chat.id, "Обраний об'єм двигуна: " + eng)
        print(eng)
        price(call.message)
    else:
        bot.send_message(call.message.chat.id, 'Обрана потужність двигуна: ' + eng)
        print(eng)
        price(call.message)


@bot.message_handler(content_types=["text"])
def price(message):
    mark = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text="До 470 тис. грн.", callback_data="До 470 тис. грн.")
    button2 = telebot.types.InlineKeyboardButton(text="До 720 тис. грн.", callback_data="До 720 тис. грн.")
    button3 = telebot.types.InlineKeyboardButton(text="Понад 720 тис. грн.", callback_data="Понад 720 тис. грн.")
    button4 = telebot.types.InlineKeyboardButton(text="Назад", callback_data="Назад")
    button5 = telebot.types.InlineKeyboardButton(text="На початок", callback_data="На початок")
    mark.add(button1, button2, button3, button4, button5)
    bot.send_message(message.chat.id, "Оберіть вартість авто", reply_markup=mark)


@bot.callback_query_handler(func=lambda call: call.data in prices)
def query_enginetype(call):
    bot.answer_callback_query(callback_query_id=call.id)
    global pr
    pr = call.data
    bot.send_message(call.message.chat.id, 'Обрана вартість авто: ' + pr)
    print(pr)
    info(call.message)


@bot.message_handler(content_types=["text"])
def info(message):
    bot.send_message(message.chat.id, 'Отже ви вибрали:\n' + 'Бренд: ' + br + '\n' + 'Модель: ' +
                     mod + '\n' + 'Рік випуску: ' + yer + '\n' + 'Тип двигуна: ' + ent.lower() + '\n' + "Потужність/Об'єм двигуна: " + eng + '\n' +
                     'Вартість авто: ' + pr.lower())


bot.polling()
