import telebot
import os
from datetime import datetime, timedelta

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

def get_countdown():
    # Добавляем 3 часа к времени сервера, чтобы получить МСК
    now = datetime.utcnow() + timedelta(hours=3)
    year = now.year
    
    seasons = [
        ("Весны 🌸", datetime(year if now < datetime(year, 3, 1) else year + 1, 3, 1)),
        ("Лета ☀️", datetime(year if now < datetime(year, 6, 1) else year + 1, 6, 1)),
        ("Осени 🍂", datetime(year if now < datetime(year, 9, 1) else year + 1, 9, 1)),
        ("Зимы ❄️", datetime(year if now < datetime(year, 12, 1) else year + 1, 12, 1)),
    ]
    
    seasons.sort(key=lambda x: x[1])
    
    res = "📅 **До начала сезонов осталось (по МСК):**\n\n"
    for name, d in seasons:
        diff = d - now
        days = diff.days
        hours = diff.seconds // 3600
        minutes = (diff.seconds // 60) % 60
        res += f"{name}: {days}д. {hours}ч. {minutes}мин.\n"
    
    return res

@bot.message_handler(commands=['how'])
def how(m):
    bot.send_message(m.chat.id, get_countdown(), parse_mode="Markdown")

if __name__ == "__main__":
    bot.infinity_polling()
