import pyrogram
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message, ChatMember
from pyrogram.raw.types.bot_command import BotCommand
from typing import List
from utils import *


bot = pyrogram.Client('matcom-bot', bot_token=open('token').read())


start_cmd = BotCommand(command = 'start', description = 'Start the bot')
info_cmd = BotCommand(command = 'info', description = 'Show official chats')


cmds_list = [start_cmd, info_cmd]

#region Commands

@bot.on_message(filters.command(['start'])) #finished
def send_welcome(client: Client, message: Message):

    if is_private(message):
        if check_status('started', message.from_user.id):
            
            bot.send_message(
                message.chat.id,
                'Usted ya ha iniciado el bot.',
                disable_web_page_preview=True
            )
        else:        
            bot.send_message(
                message.chat.id,
                '🖖 Hola! Bienvenido al chatbot de MatCom!',
                disable_web_page_preview=True
            )
            
            add_status(message.from_user.id, 'started')
        
        return
        
    bot.send_message(
        message.chat.id,
        'Este comando no está disponible en este chat.',
        disable_web_page_preview=True
    )
        

@bot.on_message(filters.command(['help'])) #finished
def send_commands_info(client: Client, message: Message):
    
    if is_unauthorized(message):
        return
    
    if is_private(message):
            
        cmds = get_commands_info(cmds_list)
        
        bot.send_message(
            message.chat.id,
            cmds,
            disable_web_page_preview=True
        )
        return
        
    bot.send_message(
        message.chat.id,
        'Este comando no está disponible en este chat.',
        disable_web_page_preview=True
    )
    

@bot.on_message(filters.command(['info'])) #finished
def show_channels(client: Client, message: Message):
    
    if is_unauthorized(message):
        return
    
    if not is_private(message):
        bot.send_message(
            message.chat.id,
            'Este comando no está disponible en este chat.',
            disable_web_page_preview=True
        )
        
        return
    
    text = message.text.split()
    if(len(text) == 1):
        bot.send_message(
            message.chat.id,
            'A cual carrera perteneces:',
            disable_web_page_preview=True,
            reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        'Matemática',
                        callback_data = 'm'
                    ),
                    InlineKeyboardButton(
                        'Computación',
                        callback_data = 'cc'
                    )
                ]
            ]
            )
        )
    else:
        bot.send_message(
            message.chat.id,
            get_general_chats() + '\n' + get_specific_chats(text[1]),
            disable_web_page_preview=True
        )


@bot.on_message(filters.command(['authenticate'])) #finished
def authenticate_user(client: Client, message: Message):
    if is_private(message):
        if check_status('authenticated', message.from_user.id):
            bot.send_message(
            message.chat.id,
            'Usted ya se encuentra autenticado.',
            disable_web_page_preview=True
            )
        elif check_status('pending', message.from_user.id):
            bot.send_message(
            message.chat.id,
            'Su autenticación está pendiente, por favor escriba el código que fue enviado a su correo.',
            disable_web_page_preview=True
            )
        else:
            bot.send_message(
            message.chat.id,
            'Por favor proporcione su dirección de correo de MATCOM.',
            disable_web_page_preview=True
            )
    else:
        bot.send_message(
            message.chat.id,
            'Este comando no está disponible en este chat.',
            disable_web_page_preview=True
        )


@bot.on_message(filters.command(['notify'])) #finished
def notify_users(client: Client, message: Message):
    
    if is_private(message):
        bot.send_message(
            message.chat.id,
            'Este comando no está disponible en este chat.',
            disable_web_page_preview=True
        )
        return
    
    if not is_admin(message.chat.id, message.from_user.id):
        bot.send_message(
            message.chat.id,
            'Usted no puede usar este comando.',
            disable_web_page_preview=True
        )
        return
    
    chat_text = ('Por favor, todos los integrantes del chat, '
                f'favor de registrarse en este bot en caso de no estarlo. '
                'De no hacerlo en un tiempo será eliminado de este grupo por '
                'nuevas políticas de los administradores.')
    
    bot.send_message(
            message.chat.id,
            chat_text,
            disable_web_page_preview=True
        )


@bot.on_message(filters.command(['delete_users'])) #finished
def delete_users(client: Client, message: Message):
    
    if is_private(message):
            
        bot.send_message(
            message.chat.id,
            'Este comando no está disponible en este chat.',
            disable_web_page_preview=True
        )
        
        return

    admins = bot.get_chat_members(message.chat.id, filter = 'administrators')
    
    if not is_admin(message.chat.id, message.from_user.id, admins):
        bot.send_message(
            message.chat.id,
            'Usted no puede usar este comando.',
            disable_web_page_preview=True,
        )
        
        return

    for member in bot.iter_chat_members(message.chat.id):
        if not (member in admins or member.user.is_bot):
            if not check_status('authenticated', member.user.id):
                bot.kick_chat_member(message.chat.id, member.user.id)


@bot.on_message(filters.command(['clear'])) #finished
def clear_chat(client: Client, message: Message):
    
    if is_private(message):
            
        bot.send_message(
            message.chat.id,
            'Este comando no está disponible en este chat.',
            disable_web_page_preview=True
        )
        
        return
            
    
    admins = bot.get_chat_members(message.chat.id, filter = 'administrators')
    
    if not is_admin(message.chat.id, message.from_user.id, admins):
        bot.send_message(
            message.chat.id,
            'Usted no puede usar este comando.',
            disable_web_page_preview=True,
        )
        
        return
    
    for member in bot.iter_chat_members(message.chat.id):
        if not (member in admins or member.user.is_bot):
            bot.kick_chat_member(message.chat.id, member.user.id)

#endregion

#region

@bot.on_message(filters.regex('(@estudiantes.matcom.uh.cu|@matcom.uh.cu)'))
def send_email(client: Client, message: Message):
    
    code = send_code(message.text)
    
    add_status(message.from_user.id, 'pending', code, message.text)
    
    bot.send_message(
        message.chat.id,
        'Se ha enviado un código de verificación a su dirección de correo, por favor escriba el código aquí.',
        disable_web_page_preview=True
        )
    

@bot.on_message(filters.regex('[0-9]{6}'))
def validate_authentication(client: Client, message: Message):
    
    values, status = check_authentication(message.from_user.id, int(message.text))
    if status:
        bot.send_message(
            message.chat.id,
            'Usted se ha autenticado con éxito.',
            disable_web_page_preview=True,
        )
        
        add_status(message.from_user.id, 'authenticated', email= values[1])
        
    else:
        bot.send_message(
            message.chat.id,
            'Código incorrecto.',
            disable_web_page_preview=True,
        )   


@bot.on_message(filters.regex("#doc")) #finished
def pin_document(client: Client, message: Message):
    
    if (not is_private(message)) and is_admin(message.chat.id, message.from_user.id):
        message.pin()
        
        
@bot.on_message(filters.regex("#info")) #finished
def pin_document(client: Client, message: Message):
    
    if (not is_private(message)) and is_admin(message.chat.id, message.from_user.id):
        message.pin()

#endregion

#region Auxiliary Functions

def is_unauthorized(message: Message):
    
    status = not check_status('authenticated', message.from_user.id)
    
    if status:
        bot.send_message(
            message.chat.id,
            'Primero debe autenticarse.',
            disable_web_page_preview=True
        )
    return status


def is_admin(chat_id: int, user_id: int, admins: List[ChatMember] = None):
    
    if admins == None:
        admins = bot.get_chat_members(chat_id, filter = 'administrators')
    
    for i in admins:
        if i.user.id == user_id:
            return True
    
    return False

#endregion

#region CallbackQueries

@bot.on_callback_query(filters.regex('^(cc|m)$'))
def info_answer(client: Client, callback_query: CallbackQuery):
    if(callback_query.data == 'cc'):
        bot.send_message(
            callback_query.message.chat.id,
            'Que año cursas:',
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        'Primer Año',
                        callback_data = 'cc1'
                    ),
                    InlineKeyboardButton(
                        'Segundo Año',
                        callback_data = 'cc2'
                    )
                ],
                [
                    InlineKeyboardButton(
                        'Tercer Año',
                        callback_data = 'cc3'
                    ),
                    InlineKeyboardButton(
                        'Cuarto Año',
                        callback_data = 'cc4'
                    )
                ]
            ]
            )
        )
    else:
        bot.send_message(
            callback_query.message.chat.id,
            'Que año cursas:',
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        'Primer Año',
                        callback_data = 'm1'
                    ),
                    InlineKeyboardButton(
                        'Segundo Año',
                        callback_data = 'm2'
                    )
                ],
                [
                    InlineKeyboardButton(
                        'Tercer Año',
                        callback_data = 'm3'
                    ),
                    InlineKeyboardButton(
                        'Cuarto Año',
                        callback_data = 'm4'
                    )
                ]
            ]
            )
        )   


@bot.on_callback_query(filters.regex('^(cc[1234]|m[1234])$'))
def year_info(client: Client, callback_query: CallbackQuery):
    bot.send_message(
        callback_query.message.chat.id,
        get_specific_chats(callback_query.data),
        disable_web_page_preview= True
    )
  
#endregion  

bot.start()
pyrogram.idle()
bot.stop()
