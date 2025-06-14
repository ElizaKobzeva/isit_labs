import telebot
from telebot import types
import requests
import xml.etree.ElementTree as ET
import datetime
from datetime import date

bot = telebot.TeleBot("7687972992:AAGJNdajKIHbcYNGPm7fPX1aWKYrpAAILlk")  # 🔁 Замените на токен своего бота

# Список поддерживаемых валют (код валюты: код ЦБ РФ)
CURRENCIES = {
    "USD": "R01235",
    "EUR": "R01239"
}

# Словарь для хранения выбранной валюты по chat_id
user_state = {}


def validate_date(input_date_str):
    try:
        input_date = datetime.datetime.strptime(input_date_str, "%d.%m.%Y").date()
        if input_date > date.today():
            return None
        return input_date
    except ValueError:
        return None


def get_currency_rate(currency_id, date_req):
    try:
        url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={date_req.strftime('%d/%m/%Y')}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.text)

        # Получаем дату курса
        actual_date = root.attrib.get("Date", date_req.strftime("%d.%m.%Y"))

        # Ищем нужную валюту
        for valute in root.findall("Valute"):
            if valute.attrib["ID"] == currency_id:
                nominal = valute.find("Nominal").text
                name = valute.find("Name").text
                value = valute.find("Value").text.replace(",", ".")
                return {
                    "date": actual_date,
                    "nominal": nominal,
                    "name": name,
                    "value": value
                }
        return None
    except (requests.RequestException, ET.ParseError) as e:
        print(f"Error fetching currency rate: {e}")
        return None


@bot.message_handler(commands=['start', 'help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*CURRENCIES.keys())
    bot.send_message(message.chat.id, "Выберите валюту:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in CURRENCIES)
def choose_currency(message):
    user_state[message.chat.id] = {"currency": message.text}
    bot.send_message(message.chat.id, "Теперь введите дату в формате ДД.ММ.ГГГГ:")


@bot.message_handler(func=lambda message: True)
def handle_date(message):
    chat_id = message.chat.id
    if chat_id not in user_state or "currency" not in user_state[chat_id]:
        bot.send_message(chat_id, "Сначала выберите валюту, нажав /start.")
        return

    # Проверяем дату
    input_date = validate_date(message.text)
    if not input_date:
        bot.send_message(chat_id, "Неверная дата. Введите дату в формате ДД.ММ.ГГГГ (не будущую дату).")
        return

    # Получаем данные о валюте
    currency_name = user_state[chat_id]["currency"]
    currency_data = get_currency_rate(CURRENCIES[currency_name], input_date)

    if not currency_data:
        bot.send_message(chat_id, f"Не удалось получить курс {currency_name} на указанную дату.")
        return

    # Форматируем ответ
    response = (f"Курс ЦБ РФ на {currency_data['date']}:\n"
                f"{currency_data['nominal']} {currency_data['name']} = {currency_data['value']} руб.")

    bot.send_message(chat_id, response)


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling()