import json
import pyrogram
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.types.bots_and_keyboards import callback_query
from utils import get_specific_chats, get_general_chats
import sys


bot = pyrogram.Client("matcom-bot", bot_token=open("token").read())


@bot.on_message(filters.command(['start', 'help']))
def send_welcome(client, message: pyrogram.types.Message):
    bot.send_message(
        message.chat.id,
        "🖖 Hola! Bienvenido al chatbot de MatCom!",
        disable_web_page_preview=True
    )


@bot.on_message(filters.command(['info']))
def show_channels(client, message:pyrogram.types.Message):
    text = message.text.split()
    if(len(text) == 1):
        bot.send_message(
            message.chat.id,
            "A cual carrera perteneces:",
            disable_web_page_preview=True,
            reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Matemática",
                        callback_data = "m"
                    ),
                    InlineKeyboardButton(
                        "Computación",
                        callback_data = "cc"
                    )
                ]
            ]
            )
        )
    else:
        bot.send_message(
            message.chat.id,
            get_general_chats() + "\n" + get_specific_chats(text[1]),
            disable_web_page_preview=True,
        )


@bot.on_callback_query(filters.regex("^(cc|m)$"))
def info_answer(client, callback_query:CallbackQuery):
    if(callback_query.data == "cc"):
        bot.send_message(
            callback_query.message.chat.id,
            "Que año cursas:",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Primer Año",
                        callback_data = "cc1"
                    ),
                    InlineKeyboardButton(
                        "Segundo Año",
                        callback_data = "cc2"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Tercer Año",
                        callback_data = "cc3"
                    ),
                    InlineKeyboardButton(
                        "Cuarto Año",
                        callback_data = "cc4"
                    )
                ]
            ]
            )
        )
    else:
        bot.send_message(
            callback_query.message.chat.id,
            "Que año cursas:",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Primer Año",
                        callback_data = "m1"
                    ),
                    InlineKeyboardButton(
                        "Segundo Año",
                        callback_data = "m2"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Tercer Año",
                        callback_data = "m3"
                    ),
                    InlineKeyboardButton(
                        "Cuarto Año",
                        callback_data = "m4"
                    )
                ]
            ]
            )
        )
        
@bot.on_callback_query(filters.regex("^(cc[1234]|mm[1234])$"))
def year_info(client, callback_query:CallbackQuery):
    bot.send_message(
        callback_query.message.chat.id,
        get_specific_chats(callback_query.data),
        disable_web_page_preview= True
    )
    

bot.start()
pyrogram.idle()
bot.stop()
