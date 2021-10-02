# импортирование нужной библиотеки
# и других необходимых элементов из файлов
import telebot
from config import TOKEN, keys
from extensions import Converter, APIException

# создание объекта bot
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_instruction(message: telebot.types.Message):
    text = "Для начала работы, введите команду в следующем формате: \n" \
           "< имя валюты >" \
           "< в какую валюту перевести >" \
           "< количество переводимой валюты >" \
           "\n Чтобы увидить список валют, введите: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = list(map(str.lower, message.text.split()))
    try:
        result = Converter.convert(values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Цена {values[2]} {values[0]} в {values[1]} составляет: {result} {keys[values[1]]}'
        bot.send_message(message.chat.id, text)


bot.polling()








