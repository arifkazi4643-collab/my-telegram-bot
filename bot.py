import os
import telebot
import requests
import random
from flask import Flask
from threading import Thread

# Flask Server setup binding error hatane ke liye
app = Flask('')
@app.route('/')
def home(): return "98 Pay AI Assistant is active!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Environment Tokens
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
bot = telebot.TeleBot(BOT_TOKEN)

# App Data Context for Groq AI
APP_PROMPT = """
You are a helpful, empathetic, and 100% human-like group manager for the app '98 pay'. Do not act like a robot. Speak in natural Hinglish.
Here are the absolute facts about the app '98 pay':
- App Name: 98 pay. Purpose: Users come here to earn money.
- Add UPI Setup: Users must click 'add upi' and add tools like:
  * Mobikwik (side text: only buy and sell)
  * Airtel (only sell)
  * Paytm Business (only sell)
  * PhonePe (only sell)
- How to add tool step-by-step: Click 'add upi' -> Choose tool (e.g., Mobikwik) -> Enter registered mobile number -> Click 'send otp' -> Copy-paste OTP -> Select UPI ID -> Tool added successfully. Repeat for all.
- Buy System: After adding tools, users see 'buy' on screen. Click buy -> see orders and prices. Example: For a 1000 order via Mobikwik, select Mobikwik and grab the order -> click pay -> automatically opens Mobikwik -> enter MPIN to pay -> take screenshot of payment history -> upload screenshot in 98pay -> order succeeds in 30 seconds -> balance updates.
- Commission: 98pay gives 3% + ₹6 instant commission on every order. (e.g., 1000 order reflects as 10036 in My Balance). Buy starts from ₹100.
- Sell/Withdraw System: Sell happens automatically. Minimum/Lowest sell amount is ₹200. If balance is below 200, sell/withdraw is impossible.
- Handling Low Balance Complaints: Explain positively that minimum sell requires ₹200. Encourage them to do more buy orders starting from ₹100 to reach the threshold.
- Handling Negative/Abusive users: Always remain polite, positive, and professionally counter any bad-mouthing with clear facts about high commissions and automatic payouts.
- Extra Sections: 'Buy History' tracks bought orders. 'Sell History' tracks withdrawals. 'Newbie Bonus' is ₹200 available in the Bonus Center after completing simple tasks.
- Sell Related Issues (Slow Sell): If anyone complains about slow sell, tell them creatively (do not repeat verbatim but keep meaning same): "Hlw brother apka sell esliye slow ho gaya hai kyuki apne ek hi upi se bar bar sell de rahe ho, please upi id change karo. Problem solve na ho toh rebind karo, ya phir upi toll delete karke firse add karo. First sell ke liye Airtel ya PhonePe use karo, highly recommended hai."
- Unresolved issues: If a query is too complex or out of your knowledge base, politely and awesomely guide them to contact the real admins: @Ownerrrrx_01, @pay98_Sanben, @BROKENBOYxERA, or @Lootisbsi.
- Download Link Requirement: If anyone asks for the link, give the official link: https://98pay.in in a beautiful format.
"""

# 1. New Member Welcome Handler (Fixed to mention new users dynamically)
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for member in message.new_chat_members:
        if member.id != bot.get_me().id:
            name = member.first_name
            username = member.username
            mention = f"@{username}" if username else name
            welcome_responses = [
                f"Welcome dear {mention}! Kyse ho? group me aapka swagat hai! ❤️",
                f"Hey {mention}, welcome dear! Kaise ho aap? 98 pay group me aapka swagat hai ✨",
                f"Welcome dear {mention}! Kyse ho bro? 98 pay me earning start karne ke liye ready ho jao! 🎉"
            ]
            bot.reply_to(message, random.choice(welcome_responses))

# 2. Photo/Screenshot Reply Handler
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo_reply = (
        "WAIT DEAR CHECKING ❤️❤️❤️\n"
        "FOR MORE HELP PLEASE CONTACT ADMIN\n"
        "@Ownerrrrx_01\n"
        "@pay98_Sanben\n"
        "@BROKENBOYxERA\n"
        "@Lootisbsi\n"
        "❤️❤️❤️❤️"
    )
    bot.reply_to(message, photo_reply)

# 3. Smart AI Message Handler (Replies to everything open-minded)
@bot.message_handler(func=lambda msg: True, content_types=['text'])
def handle_ai_response(message):
    text = message.text.lower()
    
    # Fast link execution
    if "link" in text or "app download" in text or "website" in text:
        link_templates = [
            f"🔥 **THIS IS THE OFFICIAL DOWNLOAD LINK...**\n👉 https://98pay.in \n\nEarning start karein aur 3% instant commission payein! 💰",
            f"✨ **98 Pay Official App Link:**\n🚀 https://98pay.in \n\nDownload karke Bonus Center se ₹200 ka Newbie bonus claim karna na bhoolna! ❤️"
        ]
        bot.reply_to(message, random.choice(link_templates), parse_mode="Markdown", disable_web_page_preview=True)
        return

    if not GROQ_API_KEY:
        return

    # Call AI backend to understand human patterns
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": APP_PROMPT},
                {"role": "user", "content": message.text}
            ],
            "temperature": 0.7
        }
        response = requests.post("https://groq.com", json=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            ai_reply = response.json()['choices']['message']['content']
            bot.reply_to(message, ai_reply)
    except:
        pass

if __name__ == "__main__":
    t = Thread(target=run); t.start()
    print("98Pay Humanized AI Bot is starting...")
    bot.infinity_polling()
