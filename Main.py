import telebot
import threading
import time
from datetime import datetime

# 🔹 استبدل الرمز بالـ TOKEN مالتك من BotFather
TOKEN = 8214768225:AAEMpqPVR7vYd3K97T_jFNs4m_pJ9l7kyII
bot = telebot.TeleBot(TOKEN)

reminders = []

def check_reminders():
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        for r in reminders[:]:
            if r['time'] == now:
                bot.send_message(r['chat_id'], f"⏰ تذكير: {r['text']}")
                reminders.remove(r)
        time.sleep(30)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "هلا 🙋‍♂️! أرسل لي تذكير بهالشكل:\n\nذكرني 2025-10-08 15:00 أراجع الطبيب")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("ذكرني"))
def add_reminder(message):
    try:
        parts = message.text.split(" ", 2)
        date_time = parts[1] + " " + parts[2].split(" ")[0]
        text = " ".join(parts[2].split(" ")[1:])
        reminders.append({"chat_id": message.chat.id, "time": date_time, "text": text})
        bot.reply_to(message, f"✅ تم حفظ التذكير لوقت {date_time}")
    except Exception:
        bot.reply_to(message, "❌ الصيغة خطأ. استخدم الشكل التالي:\nذكرني 2025-10-08 15:00 أراجع الطبيب")

threading.Thread(target=check_reminders, daemon=True).start()

bot.polling(non_stop=True)
