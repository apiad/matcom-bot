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


bot.start()
pyrogram.idle()
bot.stop()
