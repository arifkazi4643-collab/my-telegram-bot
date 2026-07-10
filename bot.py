import os
import telebot
import requests
import random
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "98 Pay AI Group Assistant is active!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
bot = telebot.TeleBot(BOT_TOKEN)

APP_PROMPT = """
You are a helpful, empathetic, and 100% human-like group manager for the app '98 pay'. Do not act like a robot. Speak in natural Hinglish.
Here are the absolute facts about the app '98 pay':
- App Name: 98 pay. Purpose: Users come here to earn money.
- Add UPI Setup: Users must click 'add upi' and add tools like Mobikwik (only buy and sell), Airtel (only sell), Paytm Business (only sell), PhonePe (only sell).
- How to add tool step-by-step: Click 'add upi' -> Choose tool -> Enter registered mobile number -> Click 'send otp' -> Copy-paste OTP -> Select UPI ID -> Tool added successfully.
- Buy System: Click buy -> see orders and prices. Example: For a 1000 order via Mobikwik, grab order -> click pay -> opens Mobikwik -> enter MPIN -> take screenshot of history -> upload in 98pay -> order succeeds in 30 seconds -> balance updates. Gives 3% + ₹6 instant commission (1000 becomes 10036). Buy starts from ₹100.
- Sell/Withdraw System: Sell happens automatically. Minimum/Lowest sell amount is ₹200. If balance is below 200, sell/withdraw is impossible.
- Handling Low Balance Complaints: Explain positively that minimum sell requires ₹200. Encourage them to do more buy orders.
- Handling Negative users: Always remain polite, positive, and counter bad-mouthing with clear facts.
- Extra Sections: 'Buy History', 'Sell History', 'Newbie Bonus' is ₹200 in Bonus Center after tasks.
- Sell Related Issues (Slow Sell): "Hlw brother apka sell esliye slow ho gaya hai kyuki apne ek hi upi se bar bar sell de rahe ho, please upi id change karo. Problem solve na ho toh rebind karo, ya phir upi toll delete karke firse add karo. First sell ke liye Airtel ya PhonePe use karo, highly recommended hai." (Say this creatively, do not repeat verbatim).
- Unresolved issues: Guide them to contact admins: @Ownerrrrx_01, @pay98_Sanben, @BROKENBOYxERA, or @Lootisbsi.
- Download Link: Give https://98pay.in in a beautiful format if anyone asks.
"""

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for member in message.new_chat_members:
        if member.id != bot.get_me().id:
            mention = f"@{member.username}" if member.username else member.first_name
            responses = [f"Welcome dear {mention}! Kyse ho? group me aapka swagat hai! ❤️", f"Hey {mention}, welcome dear! Kaise ho aap? 98 pay group me aapka swagat hai ✨"]
            bot.reply_to(message, random.choice(responses))

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "WAIT DEAR CHECKING ❤️❤️❤️\nFOR MORE HELP PLEASE CONTACT ADMIN\n@Ownerrrrx_01\n@pay98_Sanben\n@BROKENBOYxERA\n@Lootisbsi\n❤️❤️❤️❤️")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_group_text(message):
    text = message.text.lower()
    
    if "link" in text or "app download" in text or "website" in text:
        bot.reply_to(message, f"🔥 **THIS IS THE OFFICIAL DOWNLOAD LINK...**\n👉 https://98pay.in \n\nEarning start karein aur 3% instant commission payein! 💰", parse_mode="Markdown", disable_web_page_preview=True)
        return

    if not GROQ_API_KEY: return

    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "system", "content": APP_PROMPT}, {"role": "user", "content": message.text}],
            "temperature": 0.7
        }
        res = requests.post("https://groq.com", json=data, headers=headers, timeout=10)
        if res.status_code == 200:
            bot.reply_to(message, res.json()['choices']['message']['content'])
    except:
        pass

if __name__ == "__main__":
    t = Thread(target=run); t.start()
    bot.infinity_polling(allowed_updates=["
