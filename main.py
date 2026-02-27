import telebot
from datetime import datetime
import os

# Используем переменную окружения, чтобы не палить токен
# Если тестируешь на компе, можешь временно вставить токен в кавычки
TOKEN = os.getenv("BOT_TOKEN") 

bot = telebot.TeleBot(TOKEN)

def get_countdown():
    now = datetime.now()
    year = now.year
    
    # Даты сезонов
    dates = [
        ("Весны 🌸", datetime(year if now < datetime(year, 3, 1) else year + 1, 3, 1)),
        ("Лета ☀️", datetime(year if now < datetime(year, 6, 1) else year + 1, 6, 1)),
        ("Осени 🍂", datetime(year if now < datetime(year, 9, 1) else year + 1, 9, 1)),
        ("Зимы ❄️", datetime(year if now < datetime(year, 12, 1) else year + 1, 12, 1))
    ]
    
    dates.sort(key=lambda x: x[1])
    
    res = "📅 **Сколько осталось до сезонов:**\n\n"
    for name, d in dates:
        diff = d - now
        res += f"{name}: {diff.days} дней и {diff.seconds // 3600} часов\n"
    return res

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Привет! Жми /how, чтобы увидеть отсчет до сезонов.")

@bot.message_handler(commands=['how'])
def how(m):
    bot.send_message(m.chat.id, get_countdown(), parse_mode="Markdown")

if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling()
