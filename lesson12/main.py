from telebot import TeleBot, types
from practice.config import TOKEN, BUTTONS

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def begin(message):

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    buttons = [
        types.KeyboardButton(text=BUTTONS['go_to_inline']),
        types.KeyboardButton(text=BUTTONS['contact'], request_contact=True),
        types.KeyboardButton(text=BUTTONS['location'], request_location=True)
    ]

    kb.add(*buttons)

    bot.send_message(
        message.from_user.id,
        f'{message.from_user.first_name}, hello',
        reply_markup=kb
    )



@bot.message_handler(func=lambda m: m.text == BUTTONS['go_to_inline'], content_types=['text'])
def hello_handler(message):

    kb = types.InlineKeyboardMarkup(row_width=1)

    buttons = [
        types.InlineKeyboardButton(
            text='Я кнопка1',
            url='https://google.com'
        ),
        types.InlineKeyboardButton(
            text='Я кнопка2',
            callback_data='345'
        ),
        types.InlineKeyboardButton(
            text='Я кнопка3',
            callback_data='346'
        )
    ]

    kb.add(*buttons)

    bot.send_message(
        message.chat.id,
        f'@{message.from_user.username}, Инлайн клавиатура',
        reply_markup=kb
    )


@bot.callback_query_handler(func=lambda call: True)
def testing_inline(call):
    goods = {
        '345': {
            'title': 'Goods1',
            'desc': 'Description1'
        },
        '346': {
            'title': 'Goods1',
            'desc': 'Description1'
        }
    }

    good = goods[call.data]
    bot.send_message(
        call.message.chat.id,
        f'ві вібрали {good["title"]}, description - {good["desc"]}'
    )


@bot.message_handler(content_types=['text'])
def txt_handler(message):
    bot.send_message(
        message.from_user.id,
        f'@{message.from_user.username}, {message.text}'
    )


bot.polling()
