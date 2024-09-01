import telebot 
import shutil
from StoryTeller import StorryTeller 
from telebot import types
from DataBaseController import DataBaseController as DB
from collections import defaultdict
# start - Начать сказочное приключение
# restart - Перезапустить сказку
# button - Принудительное открытие интерфейса
# create_character - Создать персонажа
# back - Отмотать историю назад
# characters - Мои персонажи
# stories - Мои истории
# create - Создать комнату
# join - Присоединиться к комнате
# leave - Покинуть комнату
# group_chat - Управление групповым чатом
bot = telebot.TeleBot('Ваш токен')
user_states = {}
active_chats = {}
teller = None
character_prompt = "."
char_name = ""
MAX_PARTS = 3
user_id = ""



@bot.message_handler(commands=['start'])
def start_message(message):
    global user_states, teller, user_id
    user_id = message.from_user.id
    user_states = {}
    user_states[user_id] = " "
    teller = None
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
    button=types.KeyboardButton("Продолжить")
    button1 = types.KeyboardButton("Ознакомиться с пользовательским соглашением")
    markup.add(button,button1)
    bot.send_message(message.chat.id,'Привет, этот бот умеет генерировать сказочные истории при помощи современных технологий искуственного интеллекта. Продолжая, вы соглашаетесь с пользовтельским соглашением.', reply_markup=markup)


@bot.message_handler(commands=['button'])
def button_message(message):
    user_id = message.from_user.id
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
    button=types.KeyboardButton("Создать историю")
    button1=types.KeyboardButton("Мои персонажи")
    button2=types.KeyboardButton("Мои истории")
    markup.add(button, button1, button2)
    img = r'hiii.jpg' 
    text = 'Приветствуем вас в мире волшебных историй! Готовы ли окунуться в сочитание сказки и высоких технологий?'
    bot.send_photo(message.chat.id, photo=open(img, 'rb'), caption=text, reply_markup = markup)
    user_states[user_id] = " "

# @bot.message_handler(commands=['create_character'])
# def create_character(message):
    # if  message.text=="Создать персонажа":
    #     markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
    #     button=types.KeyboardButton("Подтвердить")
    #     markup.add(button)
    #     bot.send_message(message.chat.id, "Опишите персонажа", reply_markup = markup)
    #     user_id = message.from_user.id
    #     character = ''
    #     char_name = ''

    # elif message.text=="Подтвердить":
    #     bot.send_message(message.chat.id, "Введите имя персонажа")
    #     character = message.text
    #     char_name = message.text
    #     DB().add_char(user_id, char_name, character)
    #     markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
    #     button=types.KeyboardButton("Добавить персонажа")
    #     markup.add(button)
        
    #     bot.send_message(message.chat.id, "Персонаж добавлен", reply_markup = markup)

         
@bot.message_handler(commands=['restart'])
def restart(message):
   start_message(message)
   
@bot.message_handler(commands=['back'])
def back(message):
    global teller
    sost = teller.back()
    bot.send_message(message.chat.id, sost)

   
# @bot.message_handler(commands=['join_chat'])
# def join_chat(message):
#     user_id = message.from_user.id
#     if user_id in active_chats:
#         bot.send_message(message.chat.id, 'Вы уже в чате!')
#     else:
#         # Присоединяем пользователя к чату
#         active_chats[user_id] = message.from_user.username 
#         bot.send_message(message.chat.id, 'Вы присоединились к чату! Напишите "exit" для выхода.')


# @bot.message_handler(commands=['leave_chat'])
# def leave_chat(message):
#     user_id = message.from_user.id
#     if user_id in active_chats:
#         del active_chats[user_id]
#         bot.send_message(message.chat.id, 'Вы вышли из чата.')
#     else:
#         bot.send_message(message.chat.id, 'Вы не в чате.')


@bot.message_handler(commands=["characters"])
def characters(message):
    inkb = types.InlineKeyboardMarkup(row_width=1)
    
    characters = DB().get_all_chars(user_id)
    
    for character in characters:
        btn = types.InlineKeyboardButton(text=character['name'], callback_data=f"show_char_{character['id']}")
        inkb.add(btn)

    bot.send_message(message.chat.id, "Выберите персонажа:", reply_markup=inkb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("show_char_"))
def handle_character_selection(call:types.CallbackQuery):
    character_id = call.data.split("_")[-1]
    characters_list = DB().get_all_chars(user_id)
    selected_character = None
    
    # for char in characters:
    #     if char["id"] == character_id:
    #         selected_character = char

    selected_character = next((char for char in characters_list if char['id'] == character_id), None)


    back_button = types.InlineKeyboardButton(text="Назад", callback_data="back_char_")
    delete_button = types.InlineKeyboardButton(text="Удалить", callback_data=f"delete_char_{character_id}")
    choose_button = types.InlineKeyboardButton(text="Использовать", callback_data=f"choose_char_{character_id}")
    character_keyboard = types.InlineKeyboardMarkup()
    character_keyboard.add(back_button, delete_button, choose_button)
    
    bot.send_message(call.message.chat.id, f"Имя: {selected_character['name']}\nОписание: {selected_character['info']}", reply_markup=character_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_char_"))
def handle_back(call:types.CallbackQuery):
    character_id = call.data.split("_")[-1]
    DB().delete_char(user_id, character_id)
    bot.send_message(call.message.chat.id, "Персонаж удалён")
    characters(call.message)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith("choose_char_"))
def handle_back(call:types.CallbackQuery):
    global character_prompt
    character_id = call.data.split("_")[-1]
    character_prompt = DB().get_char_prompt(user_id, character_id)
    bot.send_message(call.message.chat.id, "Персонаж выбран")
    button_message(call.message)
    
@bot.callback_query_handler(func=lambda call: call.data == "back_char_")
def handle_back(call:types.CallbackQuery):
    characters(call.message)

@bot.message_handler(commands=["stories"])
def stories(message):
    inkb = types.InlineKeyboardMarkup(row_width=1)
    
    stories = DB().get_all_stories(user_id)
    
    for story in stories:
        btn = types.InlineKeyboardButton(text=story['story_name'], callback_data=f"show_story_{story['id']}")
        inkb.add(btn)

    bot.send_message(message.chat.id, "Выберите историю:", reply_markup=inkb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("show_story_"))
def handle_story_selection(call:types.CallbackQuery):
    story_id = call.data.split("_")[-1]
    stories_list = DB().get_all_stories(user_id)
    selected_story = None
    
    # for char in characters:
    #     if char["id"] == character_id:
    #         selected_character = char

    selected_story = next((story for story in stories_list if story['id'] == story_id), None)

    back_button = types.InlineKeyboardButton(text="Назад", callback_data=f"back_story_{story_id}")
    delete_button = types.InlineKeyboardButton(text="Удалить", callback_data=f"delete_story_{story_id}")
    choose_button = types.InlineKeyboardButton(text="На главную", callback_data=f"to_main")
    story_keyboard = types.InlineKeyboardMarkup()
    story_keyboard.add(back_button, delete_button, choose_button)
    media = []
    photos = selected_story["story_images"]
    
    from telebot.types import InputMediaPhoto
    for i in photos:
        data = InputMediaPhoto(open(i, 'rb'))
        media.append(data)
    bot.send_media_group(chat_id=call.message.chat.id, media = media)
    bot.send_message(call.message.chat.id, f"**{selected_story['story_name']}**\n\n\n{selected_story['story_text']}", reply_markup=story_keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_story_"))
def handle_back(call:types.CallbackQuery):
    story_id = call.data.split("_")[-1]
    DB().delete_story(user_id, story_id)
    bot.send_message(call.message.chat.id, "История удалена")
    stories(call.message)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith("back_story_"))
def handle_back(call:types.CallbackQuery):
    stories(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("to_main"))
def handle_back(call:types.CallbackQuery):
    button_message(call.message)

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

room_prompts = []
@bot.message_handler(commands=['group_chat'])
def handle_message(message):
    global counter, room_prompts
    story = None
    room_name = message.text.split(' ', 1)[1] if len(message.text.split(' ')) > 1 else None
    
    if "prompt" in message.text:
        room_prompts.append(message.text)
    print(room_prompts)
        

    for room_name, members in rooms.items():
        if message.from_user.id in members:
            for member in members:
                if member != message.from_user.id:  
                    username = message.from_user.username or "Неизвестный пользователь"
                    user_id = message.from_user.id
                    bot.send_message(member, f'Сообщение из комнаты "{room_name}" от @{username} (ID: {user_id}): {message.text}')
                    
                if len(room_prompts) >= 2:
                    for room_name, members in rooms.items():
                        if message.from_user.id in members:
                            for member in members:
                                bot.send_message(member, f'Начинаю генерировать историю...')
                    def generate_data(teller:StorryTeller, prompt:str=""):
                        part = teller.generate_story(prompt)
                        image_path = teller.generate_image()
                        return {"part":part, "image_path":image_path}
                    
                    teller= StorryTeller(". ".join(room_prompts))
                    
                    story = generate_data(teller)
                    room_prompts = []
                    
        if story != None:
            for member in members:
                bot.send_photo(message.chat.id, photo=open(story["image_path"], 'rb'))
                bot.send_message(member, f'{story["part"]}')
            story = None
                    
            # room_messages.append((room_name, message.text))
    # print(room_messages)
    if len(user_messages) == 2:
        prompt = ". ".join([i[1] for i in user_messages]) 
        print(prompt)
        # for room_name, members in rooms.items():
        #     if message.from_user.id in members:
        #         for member in members:
                    
    # print(user_messages)
@bot.message_handler(content_types='text')
def message_reply(message):
    global teller, char_name, character, character_prompt
    user_id = message.from_user.id

    if message.text == "Мои персонажи" or message.text == "Персонаж добавлен":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
        button=types.KeyboardButton("Создать персонажа")
        button2=types.KeyboardButton("Список персонажей")
        button3=types.KeyboardButton("Очистить используемого персонажа")
        markup.add(button, button2, button3)
        print(DB().get_all_chars(user_id))
        bot.send_message(message.chat.id,"""Выберите опцию\nСуществуют предсозданные персонажи.\nДля их использования нужно просто добавить его имя\nСписок доступных персонажей\n— Персонажи геншина
— Бетмен
— Фрирен (аниме)
— Джокер
— Люси (аниме)
— Макима (аниме)
— Неко Арк
— 2b""",reply_markup=markup)

    elif message.text == "Создать персонажа":
        bot.send_message(message.chat.id, "Опишите внешность персонажа")
        user_states[user_id] = "waiting_for_char_description"
        
    elif user_states[user_id] == "waiting_for_char_description":
        character = message.text
        bot.send_message(message.chat.id, "Введите имя персонажа")
        user_states[user_id] = "waiting_for_char_name"
        
    elif user_states[user_id] == "waiting_for_char_name":
        char_name = message.text
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
        button=types.KeyboardButton("Вернуться к началу")
        button2= types.KeyboardButton("Мои персонажи")
        markup.add(button,button2)
        bot.send_message(message.chat.id, "Персонаж добавлен",reply_markup=markup)
        
        DB().add_char(user_id, char_name, character)
        user_states[user_id] = " "
        

    # elif message.text=="Подтвердить описание":
    #     markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
    #     button=types.KeyboardButton("Подтвердить имя")
    #     markup.add(button)
        
    #     char_name = message.text
        
        
    # elif message.text=="Подтвердить имя":
    #     DB().add_char(user_id, char_name, character)
    #     markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
    #     button=types.KeyboardButton("Мои персонажи")
    #     button=types.KeyboardButton("Создать персонажа")
    #     markup.add(button)
    #     bot.send_message(message.chat.id, "Персонаж добавлен", reply_markup = markup)   
        
        
    elif message.text=="Ознакомиться с пользовательским соглашением":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
        button=types.KeyboardButton("Вернуться к началу")
        markup.add(button)
        bot.send_message(message.chat.id,'Пользовательское соглашение: все предоставляется по открытой лицензии и "как есть". Сгенерированный контент можно использовать в любых целях', reply_markup=markup)
        
        
    elif message.text=="Вернуться к началу":
        start_message(message)
        
        
    elif message.text=="Продолжить":
        button_message(message)

        
    elif message.text == "Создать историю":
        
        teller = None
        
        bot.send_message(message.chat.id,'О чём будет ваша история?')
        user_states[user_id] = 'waiting_for_story'
        
        
    elif user_states.get(user_id) == 'waiting_for_story':
        def generate_data(teller:StorryTeller, prompt:str=""):
            part = teller.generate_story(prompt)
            image_path = teller.generate_image()
            tts_path = teller.get_tts()
            return {"part":part, "image_path":image_path, "tts_path":tts_path}
        
        user_story = message.text
        bot.send_message(message.chat.id, f'Вы написали: {user_story}, идет генерация, подождите...')
        user_states[user_id] = " " 
        
        teller = StorryTeller(user_story, max_tryies=MAX_PARTS, character_prompt= character_prompt)
        
        firstpart = generate_data(teller, user_story)
        img = firstpart["image_path"] 
        text = firstpart["part"]
        tts = firstpart["tts_path"]
        # bot.send_photo(message.chat.id, photo=open(img, 'rb'), caption=text)
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
        button=types.KeyboardButton("Продолжить историю")
        markup.add(button)
        
        bot.send_photo(message.chat.id, photo=open(img, 'rb'))
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.send_audio(message.chat.id, audio=open(tts, 'rb'))

    elif message.text =="Продолжить историю":
        bot.send_message(message.chat.id,'Что должно произойти дальше?')
        user_states[user_id] = 'waiting_for_story2'
        

    elif user_states.get(user_id) == 'waiting_for_story2':
        def generate_data(teller:StorryTeller, prompt:str=""):
            part = teller.generate_story(prompt)
            image_path = teller.generate_image()
            tts_path = teller.get_tts()
            return {"part":part, "image_path":image_path, "tts_path":tts_path}
        
        user_story = message.text
        bot.send_message(message.chat.id, f'Вы написали: {user_story}, идет генерация, подождите...')
        user_states[user_id] = " " 
        
        firstpart = generate_data(teller, user_story)
        img = firstpart["image_path"] 
        text = firstpart["part"]
        tts = firstpart["tts_path"]
        # bot.send_photo(message.chat.id, photo=open(img, 'rb'), caption=text)
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
        button=types.KeyboardButton("Продолжить историю")
        markup.add(button)

        bot.send_photo(message.chat.id, photo=open(img, 'rb'))
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.send_audio(message.chat.id, audio=open(tts, 'rb'))
        # print(teller.get_counter())
        
        if teller.get_counter() >= MAX_PARTS:
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
            button=types.KeyboardButton("Сохранить историю")
            button1=types.KeyboardButton("Создать историю")
            button2= types.KeyboardButton("Вернуться к началу")
            markup.add(button, button1, button2)
            bot.send_message(message.chat.id, "История закончилась SADGE", reply_markup=markup)
            # user_states[user_id] = "story_ended"
        else:
            user_states[user_id] = 'waiting_for_story2'
            
    elif message.text =="Список персонажей":
        characters(message)
     
    elif message.text =="Очистить используемого персонажа":
        character_prompt = "."
        button_message(message)
        
    elif message.text =="Мои истории":
        stories(message)

    elif message.text == "Сохранить историю":
        user_states[user_id] = "saving_story"
        bot.send_message(message.chat.id, "Введите название истории")


    elif user_states[user_id] == "saving_story":
        story_name = message.text
        story_text = ". \n\n\n".join(teller.get_all_story())
        images = teller.get_all_images()
        story_images=[]
        for i in images:
            shutil.move(i, i.replace('temp','images'))
            story_images.append(i.replace('temp','images'))
        story_images = ", ".join(story_images)
        DB().add_story(user_id, story_name, story_text, story_images)
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
        button=types.KeyboardButton("Мои истории")
        button1=types.KeyboardButton("Создать историю")
        button2= types.KeyboardButton("Вернуться к началу")
        markup.add(button, button1, button2)
        bot.send_message(message.chat.id, "История сохранена", reply_markup=markup)
        
        
    # if user_id in active_chats:
    #     if message.text.lower() == "exit":
    #         leave_chat(message)
    #     else:
    #         username = message.from_user.username if message.from_user.username else "Без ника"
    #         for uid in active_chats:
    #             if uid != user_id: 
    #                 bot.send_message(uid, f'Сообщение от @{username}: {message.text}')


bot.infinity_polling()
