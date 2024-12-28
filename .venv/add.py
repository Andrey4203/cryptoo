import telebot
from config import keys, TOKEN
from utils import ConvertionException, CryptoConverter

TOKEN = '7399775640:AAHki5ffopdKmt79onhEGWwh7SdBDqFnFIM'

bot = telebot.TeleBot(TOKEN)

keys = {
    'Доллар': 'USD',
    'Эфириум': 'ETH',
    'Биткоин': 'BTC',
}


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = ('Введите команду боту в формате:\n'
            '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
        text = f'Цена {amount} {quote} в {base} = {total_base:.2f} {keys[base]}'
        bot.send_message(message.chat.id, text)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка: {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать запрос: {e}')


bot.polling()