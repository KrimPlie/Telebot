import telebot
from collections import defaultdict

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

rooms = defaultdict(set)
user_messages = []
counter = 0
room_messages = []
@bot.message_handler(commands=['create'])
def create_room(message):
    room_name = message.text.split(' ', 1)[1] if len(message.text.split(' ')) > 1 else None
    if room_name:
        rooms[room_name].add(message.from_user.id)
        bot.send_message(message.chat.id, f'Комната "{room_name}" создана! Вы присоединились к ней.')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, укажите имя комнаты.')

@bot.message_handler(commands=['join'])
def join_room(message):
    room_name = message.text.split(' ', 1)[1] if len(message.text.split(' ')) > 1 else None
    if room_name in rooms:
        rooms[room_name].add(message.from_user.id)
        bot.send_message(message.chat.id, f'Вы присоединились к комнате "{room_name}".')
    else:
        bot.send_message(message.chat.id, f'Комната "{room_name}" не найдена.')

@bot.message_handler(commands=['leave'])
def leave_room(message):
    room_name = message.text.split(' ', 1)[1] if len(message.text.split(' ')) > 1 else None
    if room_name in rooms and message.from_user.id in rooms[room_name]:
        rooms[room_name].remove(message.from_user.id)
        bot.send_message(message.chat.id, f'Вы покинули комнату "{room_name}".')
    else:
        bot.send_message(message.chat.id, f'Вы не находитесь в комнате "{room_name}".')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global counter
    if counter <2:
        user_messages.append((message.from_user.id, message.text))
        counter+=1

    for room_name, members in rooms.items():
        if message.from_user.id in members:
            for member in members:
                if member != message.from_user.id:  
                    username = message.from_user.username or "Неизвестный пользователь"
                    user_id = message.from_user.id
                    bot.send_message(member, f'Сообщение из комнаты "{room_name}" от @{username} (ID: {user_id}): {message.text}')
            room_messages.append((room_name, message.text))
    print(user_messages)
    # print(room_messages)
if __name__ == '__main__':
    bot.polling(none_stop=True)