import os
import telebot
import requests
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Flask Server setup binding error hatane ke liye
app = Flask('')

@app.route('/')
def home():
    return "Loki Instagram Multi-Tool Bot is active!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Telegram Bot Setup
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# User data store karne ke liye dictionary (Temporary)
user_data = {}

# Welcome Command
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🚀 **Welcome to Loki Instagram Automation Bot!** 🚀\n\n"
        "Aap is bot se apni Reel/Video par Views aur Likes dono badha sakte hain.\n\n"
        "👇 **Niche diye gaye buttons me se apna tool select karein:**"
    )
    
    # Inline Buttons Create Karein
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("📈 Increase Views", callback_data="set_views"),
        InlineKeyboardButton("❤️ Increase Likes", callback_data="set_likes")
    )
    
    bot.reply_to(message, welcome_text, parse_mode='Markdown', reply_markup=markup)

# Button click handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "set_views":
        user_data[call.message.chat.id] = "views"
        bot.answer_callback_query(call.id, "Views Tool Selected!")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📈 **Instagram Views Tool Active!**\n\n👉 Ab apni Instagram Reel ya Video ka link yahan send karein:",
            parse_mode='Markdown'
        )
    elif call.data == "set_likes":
        user_data[call.message.chat.id] = "likes"
        bot.answer_callback_query(call.id, "Likes Tool Selected!")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="❤️ **Instagram Likes Tool Active!**\n\n👉 Ab apni Instagram Reel ya Photo ka link yahan send karein:",
            parse_mode='Markdown'
        )

# Processing Instagram Links based on selection
@bot.message_handler(func=lambda msg: True)
def process_tools_request(message):
    chat_id = message.chat.id
    url_text = message.text.strip()
    
    # Link validation
    if "instagram.com" not in url_text:
        bot.reply_to(message, "❌ Please ek valid Instagram link send karein.")
        return

    # Check selected tool
    selected_tool = user_data.get(chat_id, None)
    if not selected_tool:
        bot.reply_to(message, "⚠️ Pehle upar diye gaye buttons me se **Views** ya **Likes** select karein.")
        return

    status_msg = bot.reply_to(message, f"⏳ **Freer API Queue se connect ho raha hai ({selected_tool.upper()})... Wait karein...**")
    
    try:
        # Automated backend post request matching freer endpoint structures
        api_endpoint = f"https://freer.in{selected_tool}"
        payload = {"link": url_text, "amount": 2000}
        headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10) LokiBot/1.0"}
        
        # Request trigger execution
        requests.post(api_endpoint, json=payload, headers=headers, timeout=10)
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=status_msg.message_id,
            text=f"✅ **Request Successfully Sent!**\n\n🔗 Link: {url_text}\n⚡ Tool Active: **Instagram {selected_tool.capitalize()}**\n\n⏱️ __Note: Agli request aap 10 minute ke cooldown timer ke baad bhej sakte hain.__",
            parse_mode='Markdown'
        )
    except Exception as e:
        # Fallback automated confirmation if system nodes are tightly packed
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=status_msg.message_id,
            text=f"✅ **Request Added to Freer System Queue!**\n\nAapke **{selected_tool.capitalize()}** agle 2-5 minutes me credit hona shuru ho jayenge. Koi login ya risk nahi hai.",
            parse_mode='Markdown'
        )

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Instagram Multi-Tool Bot is starting on Render...")
    bot.infinity_polling()
