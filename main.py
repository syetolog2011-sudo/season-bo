import telebot
import os
from datetime import datetime

# Берем токен из переменных окружения хостинга
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

def get_countdown():
    # Теперь время берется КАЖДЫЙ РАЗ при вызове функции
    now = datetime.now()
    year = now.year
    
    # Список дат начал сезонов
    seasons = [
        ("Весны 🌸", datetime(year if now < datetime(year, 3, 1) else year + 1, 3, 1)),
        ("Лета ☀️", datetime(year if now < datetime(year, 6, 1) else year + 1, 6, 1)),
        ("Осени 🍂", datetime(year if now < datetime(year, 9, 1) else year + 1, 9, 1)),
        ("Зимы ❄️", datetime(year if now < datetime(year, 12, 1) else year + 1, 12, 1)),
    ]
    
    # Сортируем, чтобы ближайший сезон был первым
    seasons.sort(key=lambda x: x[1])
    
    res = "📅 **До начала сезонов осталось:**\n\n"
    for name, d in seasons:
        diff = d - now
        days = diff.days
        hours = diff.seconds // 3600
        minutes = (diff.seconds // 60) % 60
        res += f"{name}: {days}д. {hours}ч. {minutes}мин.\n"
    
    return res

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Привет! Я бот-отсчет. Напиши /how, чтобы узнать, сколько осталось до сезонов года.")

@bot.message_handler(commands=['how'])
def how(m):
    # Бот каждый раз будет генерировать свежий текст с новым временем
    bot.send_message(m.chat.id, get_countdown(), parse_mode="Markdown")

if __name__ == "__main__":
    print("Бот запущен и готов к работе!")
    bot.infinity_polling()
