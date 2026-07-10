import os,telebot,requests,random,threading;from flask import Flask;app=Flask('');@app.route('/')
def home():return "OK"
T=os.environ.get('BOT_TOKEN');K=os.environ.get('GROQ_API_KEY');bot=telebot.TeleBot(T);P="You are a friendly, cool human group manager for '98 pay' app. Do NOT sound like an AI/robot. Use natural Hinglish words like bhai, yaar, dekho, suno, tension mat lo, bro. Keep answers short, smart, interactive. Facts: App Name is 98 pay. Earning app. Add UPI Setup: Click 'add upi' -> add Mobikwik (only buy/sell), Airtel (only sell), Paytm Business (only sell), PhonePe (only sell). Step: click add upi -> select toll -> enter registered mobile number -> send otp -> copy-paste OTP -> select UPI to bind. Buy System: Click buy -> grab order -> click pay -> automatically opens app -> enter MPIN -> screenshot history -> upload screenshot in 98pay -> success in 30s -> commission 3%+Rs6. 1000 order gives 10036. Buy starts from Rs100. Sell System: Automatic. Minimum/lowest sell is Rs 200. Under 200, sell or withdraw fails. Low balance support: Positively tell them minimum balance for sell must be 200. Encourage more buy orders starting from 100 to increase balance. Negative users: Manage them with cool patience, state high commissions facts politely, counter any bad-mouthing positively. Newbie Bonus: Rs200 in Bonus Center after tasks. Slow Sell issue logic: Explain creatively (do not repeat verbatim but meaning same): 'Hlw brother apka sell esliye slow ho gaya hai kyuki apne ek hi upi se bar bar sell de rahe ho, please upi id change karo. Problem solve na ho toh rebind karo, ya phir upi toll delete karke firse add karo. First sell ke liye Airtel ya PhonePe use karo.' Complex/Unresolved issues: Tell them to talk to admins in an awesome way: @Ownerrrrx_01, @pay98_Sanben, @BROKENBOYxERA, or @Lootisbsi. Link: Provide https://page.98pay.in/land/index.html?st=self only if asked for app link or download link."
@bot.message_handler(content_types=['new_chat_members'])
def w(m):
 for u in m.new_chat_members:
  if u.id!=bot.get_me().id:user=f"@{u.username}" if u.username else u.first_name;bot.reply_to(m,random.choice([f"Welcome dear {user}! Kaise ho bhai? Group me swagat hai! ❤️",f"Hey {user}, welcome bro! 98 pay me earning ke liye ready? ✨"]))
@bot.message_handler(content_types=['photo'])
def p(m):bot.reply_to(m,"WAIT DEAR CHECKING ❤️❤️❤️\nFOR MORE HELP PLEASE CONTACT ADMIN\n@Ownerrrrx_01\n@pay98_Sanben\n@BROKENBOYxERA\n@Lootisbsi\n❤️❤️❤️❤️")
@bot.message_handler(func=lambda m:True,content_types=['text'])
def h(m):
 t=m.text.lower()
 if "link" in t or "download" in t or "website" in t:bot.reply_to(m,random.choice(["🔥 **THIS IS THE OFFICIAL DOWNLOAD LINK...**\n👉 https://page.98pay.in/land/index.html?st=self \n\nDownload karo aur earning start karo! 💰","✨ **98 Pay Official App Link:**\n🚀 https://page.98pay.in/land/index.html?st=self \n\nDownload karke Bonus Center se ₹200 ka Newbie bonus claim karna na bhoolna! ❤️"]),parse_mode="Markdown",disable_web_page_preview=True);return
 if not K:return
 try:
  res=requests.post("https://groq.com",headers={"Authorization":f"Bearer {K}","Content-Type":"application/json"},json={"model":"llama3-8b-8192","messages":[{"role":"system","content":P},{"role": "user","content":m.text}],"temperature":0.85,"max_tokens":250},timeout=10)
  if res.status_code==200:bot.reply_to(m,res.json()['choices']['message']['content'])
 except:pass
if __name__ == "__main__":threading.Thread(target=lambda:app.run(host='0.0.0.0',port=int(os.environ.get('PORT',8080)))).start();bot.infinity_polling(allowed_updates=["message","edited_message","new_chat_members"])
