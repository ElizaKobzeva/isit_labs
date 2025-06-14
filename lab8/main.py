# -*- coding: utf-8 -*-
import telebot
from telebot import types
import random

TOKEN = '7687972992:AAGJNdajKIHbcYNGPm7fPX1aWKYrpAAILlk'
bot = telebot.TeleBot(TOKEN)

counters = {
    'Авторы': 0,
    'Жанры': 0,
    'Цитаты': 0,
    'Факты': 0,
    'Классика': 0,
    'Современное': 0,
    'Поэзия': 0,
    'Проза': 0
}

citates= ['"Привычка свыше нам дана: замена счастию она" - Пушкин "Евгений Онегин"', '"От величественного до смешного только один шаг" - Толстой "Война и мир"', '"А судьи кто?" - Грибоедов "Горе от ума"' ]
facts= ['Прадед Пушкина был африканцем', 'У Толстого был неразборчивый почерк', 'Лермонтов был суеверным' ]


def main_menu(chat_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Авторы', 'Жанры')
    keyboard.add('Цитаты', 'Факты')
    bot.send_message(chat_id, "📚 Главное меню. Выберите категорию:", reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message.chat.id)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    text = message.text
    chat_id = message.chat.id

    if text in counters:
        counters[text] += 1

    if text == 'Авторы':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Классика', 'Современное')
        keyboard.add('Вернуться в меню')
        bot.send_message(chat_id, f'Вы выбрали "Авторы" (нажато {counters["Авторы"]} раз)', reply_markup=keyboard)

    elif text == 'Жанры':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Поэзия', 'Проза')
        keyboard.add(' Вернуться в меню')
        bot.send_message(chat_id, f'Вы выбрали "Жанры" (нажато {counters["Жанры"]} раз)', reply_markup=keyboard)

    elif text == 'Цитаты':
        rand_num_citate = random.randrange(0, 3)
        bot.send_message(chat_id, f'Цитата дня 📖 (нажато {counters["Цитаты"]} раз)\n{citates[rand_num_citate]}')

    elif text == 'Факты':
        rand_num_fact = random.randrange(0, 3)
        bot.send_message(chat_id, f'Интересный факт 📚 (нажато {counters["Факты"]} раз)\n{facts[rand_num_fact]}')

    elif text == 'Классика':
        bot.send_message(chat_id, f'Классика — Пушкин, Толстой, Достоевский (нажато {counters["Классика"]} раз)')

    elif text == 'Современное':
        bot.send_message(chat_id, f'Современные авторы — Пелевин, Быков, Улицкая (нажато {counters["Современное"]} раз)')

    elif text == 'Поэзия':
        bot.send_message(chat_id, f'Поэзия — Есенин, Ахматова, Бродский (нажато {counters["Поэзия"]} раз)')

    elif text == 'Проза':
        bot.send_message(chat_id, f'Проза — Чехов, Куприн, Гоголь (нажато {counters["Проза"]} раз)')

    elif text == 'Вернуться в меню':
        main_menu(chat_id)

    else:
        bot.send_message(chat_id, "Неизвестная команда. Напиши /start для начала.")

bot.polling(none_stop=True)