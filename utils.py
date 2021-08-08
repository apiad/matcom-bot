from json import load
from os import read
from pyrogram.raw.types.bot_command import BotCommand
from pyrogram.types import Message
from typing import List
from random import randint
import smtplib


# Gets general chats
def get_general_chats():
    groups_channels = "Canales y grupos oficiales de MATCOM\n\n"
    with open("chats_info.json", encoding= "utf-8") as info:
        data = load(info)
        groups_channels += "\n".join(data[1])
    return groups_channels


def is_private(message: Message):
    return message.chat.type == 'private'


def get_specific_chats(text: str):
    result = ""
    with open("chats_info.json", encoding= "utf-8") as info:
        data = load(info)
        result += data[0][text] + "\n"
        result += "\n".join(data[2][text])
    return result


def get_commands_info(cmds_list: List[BotCommand]):
    info = "Lista de comandos:\n"
    for i in cmds_list:
        info += f"/{i.command} \t {i.description}\n"
    return info


def check_status(status_name:str, user_id: int):
    with open("users_status.json", encoding= "utf-8") as info:
        status = load(info)
        return user_id in status[status_name]


def send_email(address: str):
    email_user , email_password = '', ''
    
    with open('email') as email:
        config = email.read().split('\n')
        email_user, email_password = config[0], config[1]

    code = randint(100000, 1000000)
    
    email_text = ("Usted ha solicitado autenticarse en el bot oficial de la Facultad de Matemática y Computación.\n"
            "El siguiente código es de uso único y exclusivo.\n\n"
            f"Código:{code}")
            
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(email_user, email_password)
    server.sendmail(email_user, address, email_text.encode('utf-8'))
    server.close()
    
    return code
        