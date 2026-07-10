import os
import telebot
from flask import Flask
from threading import Thread

# Flask server banaya port binding error hatane ke liye
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Telegram Bot Setup
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! Aapka bot Web Service par bilkul perfect live chal raha hai bina kisi error ke.")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, f"Received: {message.text}")

if __name__ == "__main__":
    # Server ko background me start karein
    t = Thread(target=run)
    t.start()
    print("Bot is starting...")
    bot.infinity_polling()
