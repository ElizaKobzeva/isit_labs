import telebot
from telebot import types
from types import SimpleNamespace

bot = telebot.TeleBot("7687972992:AAGJNdajKIHbcYNGPm7fPX1aWKYrpAAILlk")

likes_by_topic = {}
dislikes_by_topic = {}

era_clicks = {
    "antiquity": 0,
    "middle_age": 0,
    "modern_time": 0,
    "contemporary": 0
}

# Словари соответствия для возврата в меню эпох
topic_to_era = {
    "detail_greece": "antiquity",
    "detail_rome": "antiquity",
    "detail_crusades": "middle_age",
    "detail_feudalism": "middle_age",
    "detail_fr_rev": "modern_time",
    "detail_colonial": "modern_time",
    "detail_ww2": "contemporary",
    "detail_space": "contemporary"
}

def back_to_main_button():
    return types.InlineKeyboardButton("🔙 Назад к выбору действия", callback_data="start_menu")

def back_to_era_button(era_code):
    return types.InlineKeyboardButton("🔙 Назад к меню эпохи", callback_data=f"return_{era_code}")

def start_menu_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📚 Исторические периоды", callback_data="main_menu"))
    markup.add(types.InlineKeyboardButton("📊 Показать статистику по эпохам", callback_data="show_era_stats"))
    return markup

def send_start_menu(chat_id):
    bot.send_message(chat_id, "Привет! Выбери действие:", reply_markup=start_menu_markup())

@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_start_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data

    if data == "start_menu":
        bot.edit_message_text("Привет! Выбери действие:", chat_id=call.message.chat.id,
                              message_id=call.message.message_id, reply_markup=start_menu_markup())

    elif data == "main_menu":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛡 Античность", callback_data="antiquity"))
        markup.add(types.InlineKeyboardButton("⚔ Средневековье", callback_data="middle_age"))
        markup.add(types.InlineKeyboardButton("🏛 Новое время", callback_data="modern_time"))
        markup.add(types.InlineKeyboardButton("🛰 Новейшее время", callback_data="contemporary"))
        markup.add(back_to_main_button())
        bot.edit_message_text("Выберите период:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif data == "show_era_stats":
        text = "📊 Статистика по эпохам:\n"
        for era, count in era_clicks.items():
            name = {
                "antiquity": "Античность",
                "middle_age": "Средневековье",
                "modern_time": "Новое время",
                "contemporary": "Новейшее время"
            }[era]
            text += f"— {name}: {count} нажатий\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=types.InlineKeyboardMarkup().add(back_to_main_button()))

    elif data in era_clicks:
        era_clicks[data] += 1
        send_era_menu(call.message.chat.id, call.message.message_id, data)

    elif data.startswith("detail_"):
        topic_key = data
        topics = {
            "detail_greece": "🏛 Древняя Греция — колыбель демократии.",
            "detail_rome": "🏛 Рим — величайшая империя всех времен.",
            "detail_crusades": "⚔ Крестовые походы — война хрситиан с мусульманами, язычниками и еретиками.",
            "detail_feudalism": "⚔ Феодализм — основа средневекового общества.",
            "detail_fr_rev": "🏛 Французская революция — продукт эпохи Просвещения.",
            "detail_colonial": "🏛 Колониализм существенно расширил географию мира.",
            "detail_ww2": "🛰 Вторая мировая — крупнейший конфликт XX века.",
            "detail_space": "🛰 Космическая гонка — СССР был первым в космосе, а США - на Луне."
        }
        text = topics.get(topic_key, "Исторический факт.")
        like = likes_by_topic.get(topic_key, 0)
        dislike = dislikes_by_topic.get(topic_key, 0)
        era_code = topic_to_era[topic_key]

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(f"👍 Нравится ({like})", callback_data=f"like_{topic_key}"),
            types.InlineKeyboardButton(f"👎 Не нравится ({dislike})", callback_data=f"dislike_{topic_key}")
        )
        markup.add(back_to_era_button(era_code))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif data.startswith("like_") or data.startswith("dislike_"):
        topic = data.split("_", 1)[1]
        if data.startswith("like_"):
            likes_by_topic[topic] = likes_by_topic.get(topic, 0) + 1
        else:
            dislikes_by_topic[topic] = dislikes_by_topic.get(topic, 0) + 1
        callback_handler(SimpleNamespace(message=call.message, data=topic))

    elif data.startswith("return_"):
        era_code = data.replace("return_", "")
        send_era_menu(call.message.chat.id, call.message.message_id, era_code)

def send_era_menu(chat_id, message_id, era_code):
    era_map = {
        "antiquity": [("Греция", "detail_greece"), ("Рим", "detail_rome")],
        "middle_age": [("Крестовые походы", "detail_crusades"), ("Феодализм", "detail_feudalism")],
        "modern_time": [("Французская революция", "detail_fr_rev"), ("Колониализм", "detail_colonial")],
        "contemporary": [("Вторая мировая война", "detail_ww2"), ("Космическая гонка", "detail_space")]
    }
    sub = types.InlineKeyboardMarkup()
    for name, cb in era_map[era_code]:
        sub.add(types.InlineKeyboardButton(name, callback_data=cb))
    sub.add(back_to_main_button())
    bot.edit_message_text("Выберите тему:", chat_id, message_id, reply_markup=sub)

bot.polling()
