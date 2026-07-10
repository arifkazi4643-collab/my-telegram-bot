import os
import telebot

# Token background se connect hoga
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Welcome Message
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 Welcome! Main aapka customized automation bot hoon.\n\n"
        "Aap jis topic par kaam karna chahte hain, mujhe batayein taaki main "
        "wahi tools aur commands yahan active kar saku."
    )
    bot.reply_to(message, welcome_text)

# Normal text handler
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, f"Received: {message.text}\nProcessing your request...")

print("Bot is ready...")
bot.infinity_polling()

