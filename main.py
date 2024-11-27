import telebot
from telebot import types

TOKEN = '7262265626:AAE4RGgwqiqU5qyWm4JkN0d9cledf_E5qY8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот кофейни. Чтобы увидеть список команд, воспользуйтесь /help.')

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Список доступных команд:\n'
                                      '/menu - выбор категории меню\n'
                                      '/wifi - информация о Wi-Fi\n'
                                      '/bot - основные команды\n'
                                      '/feedback - отправить отзыв, идею или предложение\n'
                                      '/help - отобразить это сообщение снова')

@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    categories = [('Напитки', 'drink'), ('Сытные завтраки', 'hearty_breakfast'),
                  ('Сладкие завтраки', 'sweet_breakfast')]

    for category_text, callback_data in categories:
        button = types.InlineKeyboardButton(text=category_text, callback_data=callback_data)
        markup.add(button)

    bot.send_message(message.chat.id, 'Выберите категорию меню:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['drink', 'hearty_breakfast', 'sweet_breakfast'])
def handle_category_callback(query):
    category = query.data
    photo_path = f'content/{category}.png'
    bot.send_photo(query.message.chat.id, photo=open(photo_path, 'rb'))

@bot.message_handler(commands=['wifi'])
def wifi_info(message):
    photo_path = 'content/wifi.jpg'
    wifi_description = 'Логин: `Almaty`\nПароль: `qwerty`.'
    bot.send_photo(message.chat.id, photo=open(photo_path, 'rb'), caption=wifi_description, parse_mode="MARKDOWN")

@bot.message_handler(commands=['bot'])
def bot_commands(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)

    buttons = [
        'wifi', 'наше меню',
        'контакты', 'оставить отзыв',
        'принять заказ', 'часы работы',
    ]

    for button_text in buttons:
        button = types.KeyboardButton(button_text)
        markup.add(button)

    bot.send_message(message.chat.id, 'Выберите команду:', reply_markup=markup)

@bot.message_handler(commands=['feedback'])
def activation_feedback(msg):
    bot.send_message(msg.chat.id, "Введите ваше сообщение для обратной связи:")
    bot.register_next_step_handler(msg, feedback)

def feedback(message):
    global user_message
    user_message = message.text
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    markup_inline.add(types.InlineKeyboardButton("Отправить", callback_data="confirm"),
                      types.InlineKeyboardButton("Отмена", callback_data="cancel"))
    bot.send_message(message.chat.id, f"Ваше сообщение: <b>{user_message}</b>, записано.", reply_markup=markup_inline,
                     parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data in ['confirm', 'cancel'])
def feedback_confirm(call):
    if call.data == "confirm":
        forward_chat_id = -1002125604970
        user = call.from_user
        bot.send_message(forward_chat_id,
                         f"Обратная связь от пользователя {user.first_name} (ID: {user.id} @{user.username}):\n\n{user_message}").message_id
        bot.send_message(call.message.chat.id, "Ваше сообщение успешно отправлено!")

    elif call.data == "cancel":
        help_message(call.message)

@bot.message_handler(
    func=lambda message: message.text in ['wifi', 'наше меню', 'контакты', 'оставить отзыв', 'принять заказ',
                                          'часы работы'])
def reply_buttons(message):
    if message.text == "wifi":
        wifi_info(message)
    elif message.text == "наше меню":
        menu(message)
    elif message.text == "контакты":
        contacts(message)
    elif message.text == "оставить отзыв":
        activation_feedback(message)
    elif message.text == "принять заказ":
        accept_order(message)
    elif message.text == "часы работы":
        working_hours(message)

def contacts(message):
    inline_markup = types.InlineKeyboardMarkup(row_width=2)
    gis_button = types.InlineKeyboardButton(text='2GIS', url='https://go.2gis.com/sans3')
    yandex_button = types.InlineKeyboardButton(text='Yandex.maps', url='https://yandex.kz/maps/ru/-/CDuOU4M0')
    inline_markup.add(gis_button, yandex_button)

    bot.send_photo(
        message.chat.id,
        photo='https://s9.travelask.ru/system/images/files/000/390/621/wysiwyg_jpg/maphands.jpg?1509359704',
        caption='Наш адрес: `Кунаева 130`\nНаш телефон: `+77478382703`\n',
        reply_markup=inline_markup,
        parse_mode="MARKDOWN"
    )

def accept_order(message):
    phone_number = '+77002478746'
    whatsapp_link = f'https://wa.me/{phone_number}'

    markup_inline = types.InlineKeyboardMarkup()
    whatsapp_button = types.InlineKeyboardButton(text='Заказать в WhatsApp', url=whatsapp_link)
    markup_inline.add(whatsapp_button)

    response_message = 'Мы можем принять заказ по номеру: `+7 700 247 8746`\n' \
                       'Или вы можете нам написать в WhatsApp:'

    bot.send_message(message.chat.id, response_message, reply_markup=markup_inline)

def working_hours(message):
    bot.send_message(message.chat.id, ' <b>07.30 — 23.00</b> (кухня в 08.00)', parse_mode="HTML")



# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
