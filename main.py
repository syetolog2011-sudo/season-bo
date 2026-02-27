import telebot
import os
import schedule
import time
import threading
from datetime import datetime, timedelta

# Берем токен из секретов Bothost
TOKEN = os.getenv("BOT_TOKEN")
# Твой ID (цифрами, без кавычек)
CHAT_ID = -2139050997 

bot = telebot.TeleBot(TOKEN)

def get_countdown():
    # Получаем время сервера и переводим в МСК (+3 часа)
    now = datetime.utcnow() + timedelta(hours=3)
    year = now.year
    
    seasons = [
        ("Весны 🌸", datetime(year if now < datetime(year, 3, 1) else year + 1, 3, 1)),
        ("Лета ☀️", datetime(year if now < datetime(year, 6, 1) else year + 1, 6, 1)),
        ("Осени 🍂", datetime(year if now < datetime(year, 9, 1) else year + 1, 9, 1)),
        ("Зимы ❄️", datetime(year if now < datetime(year, 12, 1) else year + 1, 12, 1)),
    ]
    
    seasons.sort(key=lambda x: x[1])
    
    res = "⏰ **Ежедневный отчет:**\n\n"
    for name, d in seasons:
        diff = d - now
        days = diff.days
        hours = diff.seconds // 3600
        minutes = (diff.seconds // 60) % 60
        res += f"{name}: {days}д. {hours}ч. {minutes}мин.\n"
    
    return res

def send_daily_stats():
    """Функция для автоматической рассылки"""
    try:
        text = get_countdown()
        bot.send_message(CHAT_ID, text, parse_mode="Markdown")
        print(f"[{datetime.now()}] Отчет успешно отправлен!")
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def run_schedule():
    """Фоновый цикл для проверки времени"""
    # 21:01 UTC — это 00:01 по Московскому времени
    schedule.every().day.at("21:01").do(send_daily_stats)
    while True:
        schedule.run_pending()
        time.sleep(30) # Проверяем каждые 30 секунд

@bot.message_handler(commands=['how'])
def how(m):
    bot.send_message(m.chat.id, get_countdown(), parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Бот готов! Я буду присылать отчет каждый день в 00:01 по МСК.")

if __name__ == "__main__":
    # Запускаем расписание в отдельном потоке, чтобы бот не завис
    threading.Thread(target=run_schedule, daemon=True).start()
    print("Система запущена. Ожидаем 00:01 МСК для рассылки...")
    bot.infinity_polling()
