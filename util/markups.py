from telebot import types


def web_app_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    # web_app = types.WebAppInfo("https://telegram.change-character.ru")
    web_app = types.WebAppInfo("https://change-character.000webhostapp.com/")
    # web_app = types.WebAppInfo("https://t.me/telegram_ai_responder?startattach")
    button = types.KeyboardButton(text="Выбор персонажа", web_app=web_app)
    keyboard.add(button)

    return keyboard


def web_app_reply():
    keyboard = types.ReplyKeyboardMarkup()
    # web_app = types.WebAppInfo("https://telegram.change-character.ru")
    web_app = types.WebAppInfo("https://change-character.000webhostapp.com/")
    # web_app = types.WebAppInfo("https://t.me/telegram_ai_responder?startattach")
    button = types.KeyboardButton(text="Выбор персонажа", web_app=web_app)
    keyboard.add(button)

    return keyboard


def data_entry():
    btn_data_entry = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_undo = types.KeyboardButton("Отмена")
    btn_data_entry.add(btn_undo)
    return btn_data_entry


def adds_user():
    btn_add_user = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_undo = types.KeyboardButton("Отмена")
    btn_add_user.add(btn_undo)
    return btn_add_user


def cancel_analyze():
    btn_full = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_undo = types.KeyboardButton('Выйти из анализа')
    btn_full.add(btn_undo)
    return btn_full
