import json
import pyrogram
import sys


bot = pyrogram.Client("matcom-bot", bot_token=open("token").read())


@bot.on_message(pyrogram.filters.command(['start', 'help']))
def send_welcome(client, message: pyrogram.types.Message):
    bot.send_message(
        message.chat.id,
        "🖖 Hola! Bienvenido al chatbot de MatCom!",
        disable_web_page_preview=True,
    )

def get_general_channels_and_groups():
    groups_channels = "Canales y grupos oficiales de MATCOM\n\n"
    with open("chats_info.json") as info:
        data = json.load(info)
        groups_channels += "\n".join(data[1])
    return groups_channels


def get_channels(text:str):
    if len(text) == 1:
        return get_general_channels_and_groups()
    result = ""
    with open("chats_info.json") as info:
        data = json.load(info)
        result += data[0][text[1]] + "\n"
        result += "\n".join(data[2][text[1]])
    return result


@bot.on_message(pyrogram.filters.command(['info']))
def show_channels(client, message:pyrogram.types.Message):
    channels = get_channels(message.text.split())
    bot.send_message(
        message.chat.id,
        channels,
        disable_web_page_preview=True,
    )

bot.start()
pyrogram.idle()
bot.stop()
