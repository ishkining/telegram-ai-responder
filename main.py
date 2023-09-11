# built-in modules
import os
import json
import logging
from datetime import datetime

# Amplitude
from amplitude import Amplitude

# Telebot
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo, \
    InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from dotenv import load_dotenv

# our functions
from util import send_amplitude_event, _make_connection, _init_tables, get_users, \
    insert_user, is_user_exist, _insert_initial_data, change_character, get_character_from_user, \
    get_response_from_chatgpt, insert_message, update_message

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

load_dotenv()

# setting amplitude
amplitude_api_key = os.environ.get('AMPLITUDE_API_KEY')
amplitude = Amplitude(amplitude_api_key)

# setting env variables of postgres
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB')

DEBUG_MODE = True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = '🤖 Приветствую тебя, рекрутера! ' \
              'Я - твой помощник в мире Python разработки, твой незаменимый телеграмм-бот! ' \
              ' Мое созидательное назначение - разрабатывать инновационных телеграмм-ботов на Python' \
              ' с использованием async и aiohttp. Я стану твоим самым верным напарником!' \
              'Так что, предстоящее собеседование - это моя территория, и я с радостью помогу тебе пройти ' \
              'его на высоком уровне. Давай работать вместе, будем создавать важные и удивительные вещи! 🚀'
    if not is_user_exist(update.effective_chat.id):
        send_amplitude_event('New User', update.effective_chat.id, amplitude)
        insert_user(update.effective_chat.id, update.effective_chat.username, update.effective_chat.first_name,
                    update.effective_chat.last_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    await update.message.reply_text(
        message,
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Выбор персонажа",
                web_app=WebAppInfo(url="https://change-character.000webhostapp.com/"),
            ),
            resize_keyboard=True
        )
    )
    print(get_users())


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Выберите персонажа:',
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Выбор персонажа",
                web_app=WebAppInfo(url="https://change-character.000webhostapp.com/"),
            ),
            resize_keyboard=True
        ),
    )


async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_html(
        text=f"Выбранный персонаж: <code>{data['character']}</code>",
        reply_markup=ReplyKeyboardRemove(),
    )
    send_amplitude_event('Change character', update.effective_chat.id, amplitude)
    change_character(update.effective_chat.id, data['character'])
    hello_character_info = get_character_from_user(update.effective_chat.id)[2]
    await update.message.reply_html(
        text=hello_character_info,
        reply_markup=ReplyKeyboardRemove(),
    )


async def gpt_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text_message = update.message.text
    character_from_user = get_character_from_user(update.effective_chat.id)
    if character_from_user:
        last_message = insert_message(update.effective_chat.id, character_from_user[0], text_message)
        send_amplitude_event('Make request', update.effective_chat.id, amplitude)

        response_gpt = get_response_from_chatgpt(text_message, role=character_from_user[1])
        send_amplitude_event('Get request', update.effective_chat.id, amplitude)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=response_gpt)
        update_message(last_message[0], response_gpt)
        send_amplitude_event('Send response', update.effective_chat.id, amplitude)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Надо сначала выбрать персонажа',
                                       reply_markup=ReplyKeyboardMarkup.from_button(
                                           KeyboardButton(
                                               text="Выбор персонажа",
                                               web_app=WebAppInfo(url="https://change-character.000webhostapp.com/"),
                                           ),
                                           resize_keyboard=True
                                       )
                                       )


def main() -> None:
    _make_connection(POSTGRES_USER, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_DB)
    _init_tables()
    _insert_initial_data()

    token = os.environ.get('TELEGRAM_API_KEY')
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    application.add_handler(MessageHandler(filters.TEXT, gpt_reply))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
