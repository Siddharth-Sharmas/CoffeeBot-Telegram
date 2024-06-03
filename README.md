Here's a detailed README file for your Telegram bot project, with descriptions in both English and Russian.

---

# Coffee Shop Bot / Бот Кофейни

This project is a Telegram bot designed to assist users with various tasks related to a coffee shop, including displaying the menu, providing Wi-Fi information, offering contact details, accepting feedback, and more.

Этот проект представляет собой Telegram-бота, предназначенного для помощи пользователям в различных задачах, связанных с кофейней, включая отображение меню, предоставление информации о Wi-Fi, предложением контактной информации, приемом отзывов и многое другое.

## Features / Функциональные Возможности

- Display menu categories / Отображение категорий меню
- Provide Wi-Fi information / Предоставление информации о Wi-Fi
- Offer main commands list / Предложение списка основных команд
- Accept and forward feedback / Прием и пересылка отзывов
- Provide contact details and map links / Предоставление контактной информации и ссылок на карту
- Show working hours / Отображение часов работы
- Accept orders via WhatsApp / Прием заказов через WhatsApp

## Getting Started / Начало Работы

### Prerequisites / Необходимые Условия

- Python 3.x
- TeleBot library (`pyTelegramBotAPI`)

### Installation / Установка

1. Clone the repository / Клонируйте репозиторий:

```bash
git clone https://github.com/your_username/coffee_shop_bot.git
cd coffee_shop_bot
```

2. Install dependencies / Установите зависимости:

```bash
pip install pyTelegramBotAPI
```

### Usage / Использование

1. Set your bot token in the code / Установите токен вашего бота в коде:

Replace `'YOUR_BOT_TOKEN_HERE'` with your actual Telegram bot token in the following line:

```python
TOKEN = 'YOUR_BOT_TOKEN_HERE'
```

2. Run the bot / Запустите бота:

```bash
python bot.py
```

### Bot Commands / Команды Бота

- `/start` - Start the bot / Запуск бота
- `/help` - Display help message / Отобразить сообщение помощи
- `/menu` - Show menu categories / Показать категории меню
- `/wifi` - Show Wi-Fi information / Показать информацию о Wi-Fi
- `/bot` - Show main commands / Показать основные команды
- `/feedback` - Send feedback / Отправить отзыв

### Detailed Code Explanation / Подробное Описание Кода

#### Bot Initialization / Инициализация Бота

```python
import telebot
from telebot import types

TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(TOKEN)
```

Initialize the bot with the provided token.

Инициализация бота с предоставленным токеном.

#### Start Command / Команда Старт

```python
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот кофейни. Чтобы увидеть список команд, воспользуйтесь /help.')
```

Send a welcome message when the `/start` command is issued.

Отправка приветственного сообщения при вводе команды `/start`.

#### Help Command / Команда Помощи

```python
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Список доступных команд:\n'
                                      '/menu - выбор категории меню\n'
                                      '/wifi - информация о Wi-Fi\n'
                                      '/bot - основные команды\n'
                                      '/feedback - отправить отзыв, идею или предложение\n'
                                      '/help - отобразить это сообщение снова')
```

Provide a list of available commands.

Предоставление списка доступных команд.

#### Menu Command / Команда Меню

```python
@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    categories = [('Напитки', 'drink'), ('Сытные завтраки', 'hearty_breakfast'),
                  ('Сладкие завтраки', 'sweet_breakfast')]

    for category_text, callback_data in categories:
        button = types.InlineKeyboardButton(text=category_text, callback_data=callback_data)
        markup.add(button)

    bot.send_message(message.chat.id, 'Выберите категорию меню:', reply_markup=markup)
```

Display menu categories with inline buttons.

Отображение категорий меню с использованием инлайн-кнопок.

#### Callback Handler for Menu / Обработчик Callback для Меню

```python
@bot.callback_query_handler(func=lambda call: call.data in ['drink', 'hearty_breakfast', 'sweet_breakfast'])
def handle_category_callback(query):
    category = query.data
    photo_path = f'content/{category}.png'
    bot.send_photo(query.message.chat.id, photo=open(photo_path, 'rb'))
```

Handle category selection and display the appropriate image.

Обработка выбора категории и отображение соответствующего изображения.

#### Wi-Fi Information / Информация о Wi-Fi

```python
@bot.message_handler(commands=['wifi'])
def wifi_info(message):
    photo_path = 'content/wifi.jpg'
    wifi_description = 'Логин: `Almaty`\nПароль: `qwerty`.'
    bot.send_photo(message.chat.id, photo=open(photo_path, 'rb'), caption=wifi_description, parse_mode="MARKDOWN")
```

Provide Wi-Fi information.

Предоставление информации о Wi-Fi.

#### Bot Commands / Основные Команды

```python
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
```

Display a list of main commands using custom keyboard.

Отображение списка основных команд с использованием пользовательской клавиатуры.

#### Feedback Handling / Обработка Отзывов

```python
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
```

Prompt the user to enter feedback and confirm or cancel the submission.

Запрос у пользователя на ввод отзыва и подтверждение или отмена отправки.

#### Contact Information / Контактная Информация

```python
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
```

Provide contact information and map links.

Предоставление контактной информации и ссылок на карту.

#### Accept Orders / Принять Заказы

```python
def accept_order(message):
    phone_number = '+77002478746'
    whatsapp_link = f'https://wa.me/{phone_number}'

    markup_inline = types.InlineKeyboardMarkup()
    whatsapp_button = types.InlineKeyboardButton(text='Заказать в WhatsApp', url=whatsapp_link)
    markup_inline.add(whatsapp_button)

    response_message = 'Мы можем принять заказ по номеру: `+7 700 247 8746`\n' \
                       'Или вы можете нам написать в WhatsApp:'

    bot.send_message(message.chat.id, response_message, reply_markup=markup_inline)
```

Provide order acceptance details with a WhatsApp link.

Предоставление информации о приеме заказов со ссылкой на WhatsApp.

#### Working Hours / Часы Работы

```python
def working_hours(message):
    bot.send_message(message.chat.id, ' <b>07.30 — 23.00</b> (кухня в 08.00)', parse_mode="HTML")
```

Display the working hours of the coffee shop.

Отображение часов работы кофейни.

### Running the Bot / Запуск Бота

```python
if __name__ == "__main__":
    bot.polling(none_stop=True)
```

Start the bot with polling.
