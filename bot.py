import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 16852082638  # Твой ID администратора

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(message, "Привет! Напиши своё сообщение.")


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
  # Если сообщение написал ты (админ) и это ответ на пересланное сообщение
  if message.from_user.id == ADMIN_ID and message.reply_to_message:
    try:
      replied_text = message.reply_to_message.text
      if "ID:" in replied_text:
        # Достаем ID пользователя из текста уведомления
        parts = replied_text.split("ID:")
        user_id = int(parts[1].split("\n")[0].strip())
        # Отправляем ответ пользователю от имени бота
        bot.send_message(user_id, f"Сообщение от администратора:\n{message.text}")
        bot.reply_to(message, "Ответ успешно доставлен!")
        return
    except Exception as e:
      bot.reply_to(message, f"Ошибка при отправке: {e}")
      return

  # Если пишет обычный пользователь — пересылаем тебе с его данными
  user = message.from_user
  username = f"@{user.username}" if user.username else "нет юзернейма"
  name_text = f"{user.first_name} {user.last_name or ''}".strip()

  admin_notification = (
      f"📥 Новое сообщение!\n\n"
      f"От: {name_text} ({username})\n"
      f"ID: {user.id}\n\n"
      f"Текст:\n{message.text}"
  )

  bot.send_message(ADMIN_ID, admin_notification)


if __name__ == "__main__":
  bot.infinity_polling()
