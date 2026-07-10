import os, telebot, random, threading
from flask import Flask

app = Flask('')
@app.route('/')
def home(): return "Loki FFMAX Guild Manager Live"

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# In-memory session datastore to track guild scores
guild_players = {}

@bot.message_handler(commands=['start', 'help'])
def start_guild_bot(m):
    text = (
        "🛡️ **Free Fire MAX Professional Guild Glory Manager v1** 🛡️\n\n"
        "Welcome Guild Captain! Yeh bot aapki guild me disicipline aur dog tags ko rocket ki tarah badhane me help karega.\n\n"
        "🔥 **Commands List:**\n"
        "👉 `/register [Name]` - Guild me apna naam register karein\n"
        "👉 `/addglory [Score]` - Apni daily ki points score add karein\n"
        "👉 `/leaderboard` - Dekhein sabse zyada glory kisne di\n"
        "👉 `/friday` - Friday Tournament Rules aur Task status check karein"
    )
    bot.reply_to(m, text)

@bot.message_handler(commands=['register'])
def register_user(m):
    chat_id = m.chat.id
    parts = m.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(m, "❌ Format Galat Hai! Aise likhein: `/register Arif`")
        return
    name = parts[1].strip()
    guild_players[chat_id] = {"name": name, "glory": 0}
    bot.reply_to(m, f"✅ **Success!** Aap Guild roster me `{name}` ke naam se add ho chuke hain. Ab apni glory track karne ke liye `/addglory` use karein!")

@bot.message_handler(commands=['addglory'])
def add_glory_points(m):
    chat_id = m.chat.id
    if chat_id not in guild_players:
        bot.reply_to(m, "⚠️ Pehle register karein! `/register [Naam]` likhein.")
        return
    parts = m.text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        bot.reply_to(m, "❌ Format Galat Hai! Aise likhein: `/addglory 80`")
        return
    points = int(parts[1])
    guild_players[chat_id]["glory"] += points
    bot.reply_to(m, f"🔥 `{guild_players[chat_id]['name']}` bhai ne Guild Account me **+{points} Glory** jodh di hai! Sabhi log push karte raho.")

@bot.message_handler(commands=['leaderboard'])
def show_leaderboard(m):
    if not guild_players:
        bot.reply_to(m, "📉 Roster abhi khali hai! Pehle sabhi log `/register` karein.")
        return
    # Sorting logic to rank dictionary records by highest score parameters
    sorted_players = sorted(guild_players.values(), key=lambda x: x["glory"], reverse=True)
    text = "🏆 **LIVE GUILD GLORY LEADERBOARD** 🏆\n\n"
    for i, player in enumerate(sorted_players[:10], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🎖️"
        text += f"{medal} {i}. **{player['name']}** — `{player['glory']}` Points\n"
    bot.reply_to(m, text, parse_mode='Markdown')

@bot.message_handler(commands=['friday'])
def friday_alert(m):
    tips = [
        "💡 *Glory Multiplier Tip:* Friday ko Clash Squad (CS) Match me poori 4 bande ki Guild Squad bana kar khelein, har match par sabse zyada Dog Tags milenge!",
        "💡 *Fast Dog Tag Trick:* Agar time kam hai toh full guild squad bana kar CS Mode start karein aur jaldi khatam karein, tokens turant update honge!"
    ]
    text = (
        "📆 **FRIDAY DOG TAG TOURNAMENT IS ACTIVE!** 📆\n\n"
        "Sabhi members ko aaj **minimum 80 Dog Tags** complete karne hain taaki Saturday ko custom room card mil sake!\n\n"
        f"{random.choice(tips)}\n\n"
        "👉 Apne stats update karne ke liye `/addglory` use karein!"
    )
    bot.reply_to(m, text, parse_mode='Markdown')

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))).start()
    bot.infinity_polling(allowed_updates=["message", "edited_message"])
