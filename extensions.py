import telebot
from configg import keys, TOKEN
from back import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)




#@bot.message_handler(commands = ['help'])
#def foo(message: telebot.types.Message):
#    bot.send_message(message.chat.id, 'ну типа давай сама')

@bot.message_handler(commands=['start','help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<currency name> <what currency to convert to> <amount>\n see the list of avaliable currencies: /values '
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    print(message.text)
    try:
        values= message.text.lower().split()
    
        if len(values) != 3:
            raise APIException('Неверное количество параметров')
        quote,base,amount = values
        total_base = CryptoConverter.convert(quote,base,amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:   
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)
       
@bot.message_handler()
def foo(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'hello')

print('starting...')
bot.polling()
