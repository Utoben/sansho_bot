import telebot
from telebot import types  # для указания типов
from datetime import datetime
import config

bot = telebot.TeleBot(config.token)

reminder_time = "14:00"

users_to_notify = []
users_to_not_notify = []

admin_id = 996182531

admin = "@ubelousov15"

# кнопки основного меню
def make_menu_buttons(user):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if user not in users_to_not_notify:
        btn1 = types.KeyboardButton("Что умеет бот")
        btn2 = types.KeyboardButton("Я пока не буду посещать клуб")
        btn3 = types.KeyboardButton("Тест")
        markup.add(btn1, btn2, btn3)
        return markup
    else:
        btn1 = types.KeyboardButton("Что умеет бот")
        btn2 = types.KeyboardButton("Я буду посещать клуб")
        btn3 = types.KeyboardButton("Тест")
        markup.add(btn1, btn2, btn3)
        return markup


def make_yn_come_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Да, приду")
    button2 = types.KeyboardButton("Нет, не приду")
    markup.add(button1, button2)
    return markup


def make_yn_stop_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Да, не буду приходить")
    button2 = types.KeyboardButton("Нет, не нужно")
    markup.add(button1, button2)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    users_to_notify.append(chat_id)
    print(f'users_to_notify: {users_to_notify}\n users_to_not_notify: {users_to_not_notify}')
    bot.send_message(chat_id,
                     text="Привет, {0.first_name}! Я бот кендо клуба Sansho".format(
                         message.from_user), reply_markup=make_menu_buttons(message.chat.id))


@bot.message_handler(content_types=['text'])
def func(message):
    chat_id = message.chat.id

    # описание бота
    if message.text == "Что умеет бот":
        bot.send_message(message.chat.id, text="Я бот уведомитель. Во вторник и пятницу в 14.00 буду спрашивать получится "
                                               "ли прийти на тренировку. Могу остановить уведомления и записать на "
                                               "занятие")

    # будет/не будет посещать клуб
    elif message.text == "Я пока не буду посещать клуб":

        bot.send_message(chat_id, "Остановить высыл уведомлений?",
                         reply_markup=make_yn_stop_buttons())
    elif message.text == "Я буду посещать клуб":
        if chat_id in users_to_not_notify:
            users_to_not_notify.remove(chat_id)
        if chat_id not in users_to_notify:
            users_to_notify.append(chat_id)
            print(f'Пользователь с chat_id {chat_id} {message.from_user.username} был удален из списка неоповещаемых и добавлен в список оповещаемых.  Будем '
                  f'доставать уведами')
            print(f'users_to_notify: {users_to_notify}')

        user_name = message.from_user.first_name
        user_username = message.from_user.username
        admin_message = f"Пользователь {user_name} (@{user_username}) будет ходить на тренировки."

        bot.send_message(admin_id, admin_message)
        bot.send_message(chat_id, f"Круто! Оповещаю руководителя {admin}",
                         reply_markup=make_menu_buttons(chat_id))

    # "придешь на тренировку?"
    elif message.text == "Да, приду":
        user_name = message.from_user.first_name
        user_username = message.from_user.username

        admin_message = f"Пользователь {user_name} (@{user_username}) придет на тренировку."

        bot.send_message(admin_id, admin_message)
        bot.send_message(message.chat.id, text=f"Круто. Отправляю руководителю {admin}",
                         reply_markup=make_menu_buttons(chat_id))
    elif message.text == "Нет, не приду":
        user_name = message.from_user.first_name
        user_username = message.from_user.username
        admin_message = f"Пользователь {user_name} (@{user_username}) не придет на тренировку."

        bot.send_message(admin_id, admin_message)
        bot.send_message(message.chat.id, text=f"Приходи в следующий раз. Отправляю руководителю {admin}",
                         reply_markup=make_menu_buttons(chat_id))

    # отписка от уведомлений
    elif message.text == "Да, не буду приходить":
        if chat_id not in users_to_not_notify:
            users_to_not_notify.append(chat_id)
            print(f'Пользователь с chat_id {chat_id} {message.from_user.username} был добавлен в список неоповещаемых. Ну и ладно')
            print(f'users_to_not_notify: {users_to_not_notify}')
        if chat_id not in users_to_notify:
            users_to_notify.append(chat_id)

        user_name = message.from_user.first_name
        user_username = message.from_user.username

        admin_message = (f"Пользователь {user_name} (@{user_username}) отписался от уведомлений. Ему не будут "
                         f"высылаться вопросы")

        bot.send_message(admin_id, admin_message)
        bot.send_message(message.chat.id, text=f"Уведомления останавливаем. Нажми на кнопку \'Я буду посещать клуб\' если захочешь приходить",
                         reply_markup=make_menu_buttons(chat_id))
    elif message.text == "Нет, не нужно":
        bot.send_message(message.chat.id, text="Хорошо",
                         reply_markup=make_menu_buttons(chat_id))

    # тест
    elif message.text == "Тест":

        t_send_notification(chat_id, make_yn_come_buttons())
    else:
        bot.send_message(message.chat.id, text="Такой команды я не знаю",
                         reply_markup=make_menu_buttons(chat_id))


# @bot.message_handler(content_types=['text'])
def t_send_notification(chat_id, markup):
    # chat_id = users_to_notify[message.chat.id]
    # chat_id = 0
    # for i in range(len(users_to_notify)):
    #     if users_to_notify[i] == chat_id:
    #         chat_id = chat_id
    # # chat_id = users_to_notify[0]
    bot.send_message(chat_id, "Придете на тренировку сегодня?", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_notification():
    today = datetime.now()

    if today.weekday() in [1, 4] and today.strftime("%H:%M") == reminder_time:
        for user_id in users_to_notify:
            if user_id not in users_to_not_notify:
                bot.send_message(user_id, "Придете на тренировку сегодня?", reply_markup=make_yn_come_buttons())


if __name__ == "__main__":
    while True:
        # t_send_notification()
        send_notification()
        bot.polling(none_stop=True)
