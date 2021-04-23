# Простой TelegramBot (чат-бот)
# Сперва необходимо установить pyTelegramBotAPI
# pip install pyTelegramBotAPI
import telebot

from telebot import types

# Cоздание экземпляра класса TeleBota
# Замените TOKEN своим собственным токеном API
bot = telebot.TeleBot("1738428749:AAHZjSJCENFDHfeg8OnqdaOtm2HmM1UnR8w")

# Ниже обработчики сообщений
name = ''
surname = ''
age = 0
# Обработчик сообщений, который обрабатывает входящие /start и /help команды
@bot.message_handler(commands=['start', 'help', 'Hello'])
def send_welcome(message):
	bot.reply_to(message, "Привет, гость!")
# Обработчик сообщений, который отвечает на текстовые сообщения 'привет', 'здравствуйте', 'здравствуй'
# сообщением "Давай познакомимся"
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.strip().lower() in ['привет', 'здравствуйте', 'здравствуй' ]:
        bot.reply_to(message, "Давай познакомимся")
#  Обработчик сообщений, который отвечает на текстовые сообщения 'давай', 'ок', 'хорошо'
    elif message.text.strip().lower() in ['давай', 'ок', 'хорошо' ]:
        bot.send_message(message.from_user.id, "Как тебя зовут?")
# В bot.register_next_step_handler(), передаём сообщение (message),
# и следующий шаг (вызов функции reg_name), к которому перейти после ответа пользователя.
        bot.register_next_step_handler(message, reg_name)

# Ниже Функции для перехода к следующим шагам (аналогично предыдущим)
def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Какая у вас фамилия?")
    bot.register_next_step_handler(message, reg_surname)

def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Сколько вам лет? Введите цифрами")
    bot.register_next_step_handler(message, reg_age)

def reg_age(message):
    global age
    age = int(message.text)
# Для создания кнопки (Да, Нет) используется тип InlineKeyboardMarkup
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
# При появлении сообщения
    question = 'Тебе ' + str(age) + ' лет? И тебя зовут: ' + name + ' ' + surname + '?'
# появляются кнопки (Да, Нет)
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
# Если выбрана кнопка Да
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Приятно познакомиться! Теперь сохраню Ваши данные!")
# Если выбрана кнопка Нет
    elif call.data == "no":
        global age
        age = 0
        bot.send_message(call.message.chat.id, "Попробуем еще раз!")
        bot.send_message(call.message.chat.id, "Укажите свои данные! Как тебя зовут?")
        bot.register_next_step_handler(call.message, reg_name)
# Запуск бота
bot.polling(none_stop=True)
