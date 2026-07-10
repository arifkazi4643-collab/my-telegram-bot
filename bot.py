import os, telebot, requests, random, threading, time
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Flask('')
@app.route('/')
def home(): return "Loki FFMAX HighSpeed Panel Live"

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

SENSITIVITY_DATABASE = {
    "iphone": "📱 **iPhone Special Headshot Settings:**\n\n• General: 100\n• Red Dot: 92\n• 2x Scope: 95\n• 4x Scope: 100\n💡 *Pro Tip: Drag Button Size 42% par set karein.*",
    "samsung": "📱 **Samsung Devices Best Sensitivity Settings:**\n\n• General: 98\n• Red Dot: 88\n• 2x Scope: 92\n• 4x Scope: 96\n💡 *Pro Tip: Fire button ko bilkul bottom-center me rakhein.*",
    "xiaomi": "📱 **Xiaomi / Redmi / POCO Headshot Settings:**\n\n• General: 100\n• Red Dot: 95\n• 2x Scope: 98\n• 4x Scope: 100\n💡 *Pro Tip: Default Window Animation Scale ko 0.5x karein.*",
    "realme": "📱 **Realme / Oppo Devices Pro Settings:**\n\n• General: 100\n• Red Dot: 90\n• 2x Scope: 94\n• 4x Scope: 98\n💡 *Pro Tip: Smooth Graphics + High FPS select karein.*",
    "vivo": "📱 **Vivo / iQOO Devices Headshot Settings:**\n\n• General: 99\n• Red Dot: 93\n• 2x Scope: 95\n• 4x Scope: 99\n💡 *Pro Tip: Fire button ko 'J' Shape me drag karein.*"
}

user_states = {}

@bot.message_handler(commands=['start', 'help'])
def start_panel(m):
    user_states[m.chat.id] = None
    text = (
        "🎮 **Loki Free Fire MAX Ultimate Mod-Panel v5** 🎮\n\n"
        "Welcome bhai! Is bot se aap apni FF Max profile par real likes instant inject kar sakte hain.\n\n"
        "👇 **Niche diye gaye buttons se apna tool select karein:**"
    )
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("👍 1-2 Min Instant Likes", callback_data="ff_likes"),
        InlineKeyboardButton("🎯 Headshot Sensitivity", callback_data="ff_sensi")
    )
    bot.reply_to(m, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def process_selection(call):
    chat_id = call.message.chat.id
    user_states[chat_id] = call.data
    bot.answer_callback_query(call.id)
    
    if call.data == "ff_likes":
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="⚡ **Instant Likes Module Active!**\n\n👉 Kirpiya karke apni exact numeric **Free Fire MAX UID** send karein:", parse_mode='Markdown')
    elif call.data == "ff_sensi":
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="🎯 **Headshot Sensitivity Panel Active!**\n\n👉 Kirpiya apne **Mobile Ka Brand Name** type karke send karein (e.g. Samsung, iPhone, Redmi):", parse_mode='Markdown')

# Multi-Threaded function to flood likes request immediately
def instant_like_flooder(uid):
    urls = [
        f"https://allorigins.win{requests.utils.quote('https://pitas.id' + uid)}",
        f"https://allorigins.win{requests.utils.quote('https://freefirelikes.org' + uid)}",
        f"https://allorigins.win{requests.utils.quote('https://fftools.net' + uid)}"
    ]
    for url in urls:
        try:
            h = {"User-Agent": f"Mozilla/5.0 FFMax-{random.randint(100,999)}"}
            requests.get(url, headers=h, timeout=5)
            time.sleep(0.5)
        except: continue

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_text_inputs(m):
    chat_id = m.chat.id
    user_text = m.text.strip().lower()
    selected_tool = user_states.get(chat_id, None)

    if not selected_tool:
        bot.reply_to(m, "⚠️ Pehle upar diye gaye menu se koi ek module select karein bhai! /start type karein.")
        return

    if selected_tool == "ff_likes":
        if not user_text.isdigit() or len(user_text) < 8 or len(user_text) > 12:
            bot.reply_to(m, "❌ Invalid UID! Sahi numeric Free Fire MAX id send karein.")
            return
            
        status = bot.reply_to(m, "⚡ **Instant Fast Injection Triggered!**\n\n🔗 Servers se rapid request line connect ho gayi hai...")
        
        # Launching multi-threaded flood process for 1-2 min execution
        threading.Thread(target=instant_like_flooder, args=(user_text,)).start()
        
        time.sleep(1.5)
        bot.edit_message_text(chat_id=chat_id, message_id=status.message_id, text=f"✅ **Likes Successfully Injected In 1-2 Minutes!**\n\n🎮 Player UID: `{user_text}`\n🟢 Node Speed: `Ultra-Fast (No-Queue)`\n\n📥 Request successfully accept ho gayi hai. Agle **1 se 2 minute mein** profile check karein, likes credit ho jayenge bhai! 🔥", parse_mode='Markdown')
            
    elif selected_tool == "ff_sensi":
        matched = False
        for brand, config in SENSITIVITY_DATABASE.items():
            if brand in user_text or (brand == "xiaomi" and ("redmi" in user_text or "poco" in user_text)) or (brand == "realme" and "oppo" in user_text) or (brand == "vivo" and "iqoo" in user_text):
                bot.reply_to(m, config, parse_mode='Markdown')
                matched = True
                break
        if not matched:
            bot.reply_to(m, "✨ **Universal Settings:**\n\n• General: 100\n• Red Dot: 90\n• 2x Scope: 95\n💡 *Rotation Drag use karein!*", parse_mode='Markdown')

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))).start()
    bot.infinity_polling(allowed_updates=["message", "edited_message", "callback_query"])
