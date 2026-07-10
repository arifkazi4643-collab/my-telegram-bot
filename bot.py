import os, telebot, json, threading
from flask import Flask

# Stable web server connectivity setup
app = Flask('')
@app.route('/')
def home(): return "98 Pay Native AI Active"

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Native fast responses without external complex cloud weights
RESPONSES = {
    "link": "🔥 **THIS IS THE OFFICIAL DOWNLOAD LINK...**\n👉 https://98pay.in \n\nEarning start karein aur 3% instant commission payein! 💰",
    "download": "🔥 **THIS IS THE OFFICIAL DOWNLOAD LINK...**\n👉 https://98pay.in \n\nEarning start karein aur 3% instant commission payein! 💰",
    "website": "🔥 **THIS IS THE OFFICIAL DOWNLOAD LINK...**\n👉 https://98pay.in \n\nEarning start karein aur 3% instant commission payein! 💰",
    "sell": "Hlw brother apka sell esliye slow ho gaya hai kyuki apne ek hi upi se bar bar sell de rahe ho, please upi id change karo. Problem solve na ho toh rebind karo, ya phir upi toll delete karke firse add karo. First sell ke liye Airtel ya PhonePe use karo. ❤️",
    "withdraw": "Hlw brother apka sell esliye slow ho gaya hai kyuki apne ek hi upi se bar bar sell de rahe ho, please upi id change karo. Problem solve na ho toh rebind karo, ya phir upi toll delete karke firse add karo. First sell ke liye Airtel ya PhonePe use karo. ❤️",
    "upi": "Dekho jab aap add upi pe click karke koi bhi toll add karne jayoge to apko pehle us toll (jaise mobikwik) pe tap karna hoga, apna registered number enter karna hoga, send otp pe click karke otp copy paste karna hoga, upi select karte hi toll add ho jayega! ✨",
    "buy": "Toll add karne ke baad buy pe click karein. 1000 ki order pe click karke pay karein, MPIN dalein aur us payment history ka screenshot 98pay me aakar upload kar dein! Order 30 second mai success hoke balance me 10036 show hoga (3% + ₹6 commission). 📊",
    "bonus": "98pay mai newbie bonus ₹200 hai jo aapko Bonus Center mai simple tasks ke sath diya huya hai. Jaldi claim karein! 🎉"
}

@bot.message_handler(content_types=['new_chat_members'])
def welcome(m):
    for u in m.new_chat_members:
        if u.id != bot.get_me().id:
            user = f"@{u.username}" if u.username else u.first_name
            bot.reply_to(m, f"Welcome dear {user}! Kyse ho? 98 pay group me aapka swagat hai! ❤️")

@bot.message_handler(content_types=['photo'])
def handle_photo(m):
    bot.reply_to(m, "WAIT DEAR CHECKING ❤️❤️❤️\nFOR MORE HELP PLEASE CONTACT ADMIN\n@Ownerrrrx_01\n@pay98_Sanben\n@BROKENBOYxERA\n@Lootisbsi\n❤️❤️❤️❤️")

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_text(m):
    text = m.text.lower()
    replied = False
    
    # Matching words natively with zero cloud dependencies
    for key, val in RESPONSES.items():
        if key in text:
            bot.reply_to(m, val, parse_mode="Markdown")
            replied = True
            break
            
    if not replied:
        # Custom smart general fallback logic matching human interactions
        bot.reply_to(m, "Hlw brother! Agar aapko 98pay app me buy, sell, ya upi add karne me koi dikkat hai toh baziye, ya fir direct admins ko contact karein: @Ownerrrrx_01 ✨")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))).start()
    bot.infinity_polling(allowed_updates=["message", "edited_message", "new_chat_members"])
