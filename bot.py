import pyrogram
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.raw.types.bot_command import BotCommand
from utils import *


bot = pyrogram.Client("matcom-bot", bot_token=open("token").read())


start_cmd = BotCommand(command = "start", description = "Start the bot")
info_cmd = BotCommand(command = "info", description = "Show official chats")


cmds_list = [start_cmd, info_cmd]

#region Commands

@bot.on_message(filters.command(['start']))
def send_welcome(client, message: pyrogram.types.Message):

    if is_private(message):
        bot.send_message(
            message.chat.id,
            "🖖 Hola! Bienvenido al chatbot de MatCom!",
            disable_web_page_preview=True
        )
    else:
        bot.send_message(
            message.chat.id,
            "Este comando no está disponible en este chat",
            disable_web_page_preview=True
        )
        

@bot.on_message(filters.command(['help']))
def send_commands_info(client, message: pyrogram.types.Message):
    
    if is_private(message):
        cmds = get_commands_info(cmds_list)
        
        bot.send_message(
            message.chat.id,
            cmds,
            disable_web_page_preview=True
        )
    else:
        bot.send_message(
            message.chat.id,
            "Este comando no está disponible en este chat",
            disable_web_page_preview=True
        )
    

@bot.on_message(filters.command(['info']))
def show_channels(client, message: pyrogram.types.Message):
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


@bot.on_message(filters.command(['authenticate']))
def authenticate_user(client, message: pyrogram.types.Message):
    if is_private(message):
        if check_status("authenticated", message.from_user.id):
            bot.send_message(
            message.chat.id,
            "Usted ya se encuentra autenticado",
            disable_web_page_preview=True
            )
        elif check_status("pending", message.from_user.id):
            bot.send_message(
            message.chat.id,
            "Su autenticación está pendiente, por favor escriba el código que fue enviado a su correo",
            disable_web_page_preview=True
            )
        else:
            bot.send_message(
            message.chat.id,
            "Por favor proporcione su dirección de correo de MATCOM",
            disable_web_page_preview=True
            )
    else:
        bot.send_message(
            message.chat.id,
            "Este comando no está disponible en este chat",
            disable_web_page_preview=True
        )

#endregion

#region

@bot.on_message(filters.regex("(@estudiantes.matcom.uh.cu|@matcom.uh.cu)"))
def send_code(client, message: pyrogram.types.Message):
    
    send_email(message.text)
    
    bot.send_message(
        message.chat.id,
        "Se ha enviado un código de verificación a su dirección de correo, por favor escriba el código aquí.",
        disable_web_page_preview=True
        )

#endregion

#region CallbackQueries

@bot.on_callback_query(filters.regex("^(cc|m)$"))
def info_answer(client, callback_query: CallbackQuery):
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
def year_info(client, callback_query: CallbackQuery):
    bot.send_message(
        callback_query.message.chat.id,
        get_specific_chats(callback_query.data),
        disable_web_page_preview= True
    )
  
#endregion  

bot.start()
pyrogram.idle()
bot.stop()
