from json import load
from logging import RootLogger
from pyrogram.raw.types.bot_command import BotCommand
from typing import List


# Gets general chats
def get_general_chats():
    groups_channels = "Canales y grupos oficiales de MATCOM\n\n"
    with open("chats_info.json") as info:
        data = load(info)
        groups_channels += "\n".join(data[1])
    return groups_channels


def get_specific_chats(text:str):
    result = ""
    with open("chats_info.json", encoding= "utf-8") as info:
        data = load(info)
        result += data[0][text] + "\n"
        result += "\n".join(data[2][text])
    return result


def get_commands_info(cmds_list : List[BotCommand]):
    info = "Lista de comandos:\n"
    for i in cmds_list:
        info += f"/{i.command} \t {i.description}\n"
    return info