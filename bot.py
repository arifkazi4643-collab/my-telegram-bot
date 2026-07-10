import os, telebot, requests, random, threading
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
KEY = os.environ.get('GROQ_API_KEY')
P = "You are human group manager for '98 pay' app. Speak Hinglish. Facts: App Name is 98 pay. Earn app. Add UPI: Click 'add upi' -> add Mobikwik (only buy/sell), Airtel (only sell), Paytm Business (only sell), PhonePe (only sell). Step: click add upi -> select tool -> registered number -> send otp -> paste OTP -> select UPI. Buy: Click buy -> grab order -> click pay -> automatically opens app -> enter MPIN -> screenshot history -> upload screenshot in 98pay -> success in 30s -> commission 3%+Rs6. 1000 becomes 10036. Buy starts Rs100. Sell: Automatic. Minimum sell Rs200. Under 200, sell fails. Manage negative users politely. Newbie Bonus: Rs200 in Bonus Center. Slow Sell response: 'Hlw brother apka sell esliye slow ho gaya hai kyuki apne ek hi upi se bar bar sell de rahe ho, please upi id change karo. Problem solve na ho toh rebind karo, ya phir upi toll delete karke firse add karo. First sell ke liye Airtel ya PhonePe use karo.' Admins: @Ownerrrrx_01, @pay98_Sanben, @BROKENBOYxERA, @Lootisbsi. Link: https://98pay.in"
@bot.message_handler(content_types=['new_chat_members'])
def w(m):
    for u in m.new_chat_members: 
        if u.id != bot.get_me().id: bot.reply_to(m, f"Welcome dear {f'@{u.username}' if u.username else u.first_name}! Kyse ho? ❤️")
@bot.message_handler(content_types=['photo'])
def p(m): bot.reply_to(m, "WAIT DEAR CHECKING ❤️❤️❤️\nFOR MORE HELP PLEASE CONTACT ADMIN\n@Ownerrrrx_01\n@pay98_Sanben\n@BROKENBOYxERA\n@Lootisbsi\n❤️❤️❤️❤️")
@bot.message_handler(func=lambda m: True, content_types=['text'])
def h(m):
    t = m.text.lower()
    if "link" in t or "download" in t or "website" in t:
        bot.reply_to(m, "🔥 **OFFICIAL DOWNLOAD LINK:**\n👉 https://98pay.in", parse_mode="Markdown")
        return
    if not KEY: return
    try:
        res = requests.post("https://groq.com", headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}, json={"model": "llama3-8b-8192", "messages": [{"role": "system", "content": P}, {"role": "user", "content": m.text}], "temperature": 0.7}, timeout=10)
        if res.status_code == 200: bot.reply_to(m, res.json()['choices']['message']['content'])
    except: pass
from flask import Flask
app = Flask('')
@app.route('/')
def home(): return "OK"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))).start()
bot.infinity_polling(allowed_updates=["message", "edited_message", "new_chat_members"])
