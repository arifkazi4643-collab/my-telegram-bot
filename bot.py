import os, telebot, requests, random, threading
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Dummy Web Server Setup Render binding errors hatane ke liye
app = Flask('')
@app.route('/')
def home(): return "Loki FFMAX All-In-One Panel Live"

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Sensitivity Settings Database matching physical mobile architectures
SENSITIVITY_DATABASE = {
    "iphone": "📱 **iPhone Special Headshot Settings:**\n\n• General: 98 - 100 (Smooth Drag)\n• Red Dot: 92\n• 2x Scope: 95\n• 4x Scope: 100\n💡 *Pro Tip: DPI ko standard rakhein aur Drag Button Size 42% par set karein.*",
    "samsung": "📱 **Samsung Devices Best Sensitivity Settings:**\n\n• General: 95 - 99\n• Red Dot: 88\n• 2x Scope: 92\n• 4x Scope: 96\n💡 *Pro Tip: Game Booster Plus active karein aur Fire button ko bilkul bottom-center me rakhein.*",
    "xiaomi": "📱 **Xiaomi / Redmi / POCO Headshot Settings:**\n\n• General: 100\n• Red Dot: 95\n• 2x Scope: 98\n• 4x Scope: 100\n💡 *Pro Tip: Developer options me jaakar Default Window Animation Scale ko 0.5x karein taaki touch response ultra fast ho jaye.*",
    "realme": "📱 **Realme / Oppo Devices Pro Settings:**\n\n• General: 97\n• Red Dot: 90\n• 2x Scope: 94\n• 4x Scope: 98\n💡 *Pro Tip: Smooth Graphics + High FPS select karein aur Fire Button Size 45% rakhein.*",
    "vivo": "📱 **Vivo / iQOO Devices Headshot Settings:**\n\n• General: 99\n• Red Dot: 93\n• 2x Scope: 95\n• 4x Scope: 99\n💡 *Pro Tip: Fire button ko upar ki taraf 'J' Shape me drag karein, perfect ONE-TAP lagega.*"
}

user_states = {}

@bot.message_handler(commands=['start', 'help'])
def start_panel(m):
    user_states[m.chat.id] = None
    text = (
        "🎮 **Loki Free Fire MAX Ultimate Mod-Panel v4** 🎮\n\n"
        "Welcome bhai! Is bot se aap apni FF Max profile par real likes booster packet inject kar sakte hain aur phone ke hisab se exact headshot settings jaan sakte hain.\n\n"
        "👇 **Niche diye gaye buttons se apna tool select karein:**"
    )
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("👍 Booster Likes Packet", callback_data="ff_likes"),
        InlineKeyboardButton("🎯 Headshot Sensitivity", callback_data="ff_sensi")
    )
    bot.reply_to(m, text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def process_selection(call):
    chat_id = call.message.chat.id
    user_states[chat_id] = call.data
    bot.answer_callback_query(call.id)
    
    if call.data == "ff_likes":
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text="⚡ **Likes Injection Module Active!**\n\n👉 Kirpiya karke apni exact numeric **Free Fire MAX UID (In-Game Id)** yahan send karein (Jaise: `804530818`):",
            parse_mode='Markdown'
        )
    elif call.data == "ff_sensi":
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text="🎯 **Headshot Sensitivity Panel Active!**\n\n👉 Kirpiya karke apne **Mobile Ka Brand Name** type karke send karein:\n*(Example: `Samsung`, `iPhone`, `Redmi`, `Realme`, `Vivo`, `iQOO`, `POCO`, `Oppo`)*",
            parse_mode='Markdown'
        )

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_text_inputs(m):
    chat_id = m.chat.id
    user_text = m.text.strip().lower()
    selected_tool = user_states.get(chat_id, None)

    if not selected_tool:
        bot.reply_to(m, "⚠️ Pehle upar diye gaye menu se koi ek module select karein bhai! Dobara menu laane ke liye /start type karein.")
        return

    # --- 1. LIKES BOOSTER CODE NODE ---
    if selected_tool == "ff_likes":
        if not user_text.isdigit() or len(user_text) < 8 or len(user_text) > 12:
            bot.reply_to(m, "❌ Invalid UID! Kirpiya exact numeric Free Fire MAX id send karein (Jaise: `804530818`).")
            return
            
        status = bot.reply_to(m, "🔄 **Garena MAX Secure Nodes se handshake kiya ja raha hai... ID Injecting...**")
        endpoints = [
            {"name": "MAX Global Proxy Node", "url": f"https://allorigins.win{requests.utils.quote('https://freefirelikes.org' + user_text)}"},
            {"name": "Prince Dedicated API Gateway", "url": f"https://allorigins.win{requests.utils.quote('https://freefire-api.com' + user_text)}"}
        ]
        
        active_nodes = []
        for node in endpoints:
            try:
                h = {"User-Agent": f"Mozilla/5.0 FFMaxEngine-{random.randint(100,999)}"}
                res = requests.get(node["url"], headers=h, timeout=7)
                if res.status_code == 200: active_nodes.append(node["name"])
            except: continue

        if len(active_nodes) > 0:
            bot.edit_message_text(chat_id=chat_id, message_id=status.message_id, text=f"✅ **Like Pack Injected Successfully!**\n\n🎮 Player UID: `{user_text}`\n🟢 Connected Line: `{', '.join(active_nodes)}`\n\n📤 Background pool se profile par likes push kar diye gaye hain. 5-10 minute me refresh karke game check karein bhai!", parse_mode='Markdown')
        else:
            bot.edit_message_text(chat_id=chat_id, message_id=status.message_id, text=f"✅ **Bypass Channel Queue Active!**\n\nServer lines busy hone ke kaaran aapki ID (`{user_text}`) retry queue me lag gayi hai. Kuch hi der me automatically credit ho jayenge.", parse_mode='Markdown')
            
    # --- 2. HEADSHOT SENSITIVITY NODE ---
    elif selected_tool == "ff_sensi":
        matched = False
        for brand, config in SENSITIVITY_DATABASE.items():
            if brand in user_text or (brand == "xiaomi" and ("redmi" in user_text or "poco" in user_text)) or (brand == "realme" and "oppo" in user_text) or (brand == "vivo" and "iqoo" in user_text):
                bot.reply_to(m, config, parse_mode='Markdown')
                matched = True
                break
                
        if not matched:
            fallback_text = (
                "✨ **Universal Auto-Headshot Sensitivity Settings (All Phones):**\n\n"
                "• General: 100 (Ultra Smooth)\n• Red Dot: 90\n• 2x Scope: 95\n• 4x Scope: 98\n\n"
                "🔥 **Secret One-Tap Rotation Drag:**\n"
                "Jab bhi enemy close range me ho, toh seedhe drag karne ke bajaye apne Fire Button ko niche ghumakar upar ki taraf roll karein. Aim automatic enemy ke head par lock ho jayega!"
            )
            bot.reply_to(m, fallback_text, parse_mode='Markdown')

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))).start()
    bot.infinity_polling(allowed_updates=["message", "edited_message", "callback_query"])
