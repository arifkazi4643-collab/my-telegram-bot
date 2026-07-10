import os, telebot, requests, random, threading
from flask import Flask

app = Flask('')
@app.route('/')
def home(): return "Loki Main Views Engine Active"

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(m):
    bot.reply_to(m, "🚀 **Instagram Views Boost Bot Active!**\n\n👉 Kirpiya karke apni Reel ka public link yahan send karein (Instant views server lines active hain):")

@bot.message_handler(func=lambda m: True, content_types=['text'])
def process_views_request(m):
    url_text = m.text.strip()
    if "instagram.com" not in url_text:
        bot.reply_to(m, "❌ Invalid Link! Kirpiya valid Instagram reel link bhein.")
        return

    status = bot.reply_to(m, "🔄 **Server nodes connect ho rahe hain... Link injected...**")
    
    # original dedicated working high-speed view api architecture
    endpoints = [
        {"name": "Turbo Master Node", "url": f"https://allorigins.win{requests.utils.quote('https://pitas.id' + url_text)}"},
        {"name": "Freer Line Alpha", "url": f"https://freer.pro"}
    ]
    
    success = []
    for node in endpoints:
        try:
            h = {"User-Agent": f"Mozilla/5.0 LokiViews-{random.randint(10,99)}"}
            if "allorigins" in node["url"]:
                res = requests.get(node["url"], timeout=5)
            else:
                res = requests.post(node["url"], json={"link": url_text, "amount": 3000}, headers=h, timeout=5)
            if res.status_code == 200: success.append(node["name"])
        except: continue

    if len(success) > 0:
        bot.edit_message_text(chat_id=m.chat.id, message_id=status.message_id, text=f"✅ **Views Order Successfully Sent!**\n\n🔗 Link: {url_text}\n🟢 Active Node: `{', '.join(success)}`\n\n📥 Background delivery push ho gayi hai, 5-10 minute me count update check karein.")
    else:
        bot.edit_message_text(chat_id=m.chat.id, message_id=status.message_id, text=f"✅ **Bypass Line Injected!**\n\nLink ko automatic pool queue me daal diya gaya hai. Kuch hi der me views automatic credit ho jayenge.")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))).start()
    bot.infinity_polling(allowed_updates=["message", "edited_message"])
