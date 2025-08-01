import telebot
from config import token

bot = telebot.TeleBot(token)

banned_users = {} # 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status

        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            try:
                bot.ban_chat_member(chat_id, user_id)
                bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
            except telebot.apihelper.ApiTelegramException as e:
                bot.reply_to(message, f"Не удалось забанить пользователя. Ошибка: {e}")

    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

@bot.message_handler1(func=lambda message: True)
def echo_message(message):
    if "https://" in message.text:
        user_id = message.from_user.id
        banned_users[user_id] = {
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'message_text': message.text,
            'chat_id': message.chat.id
        }
        try:
            bot.ban_chat_member(message.chat.id, user_id)
            bot.reply_to(message, f"Пользователь @{message.from_user.username} был забанен за отправку ссылок.")
        except telebot.apihelper.ApiTelegramException as e:
            bot.reply_to(message, f"Не удалось забанить пользователя. Ошибка: {e}")

    else:
        bot.reply_to(message, message.text)

bot.infinity_polling(none_stop=True)
