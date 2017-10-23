import telebot
import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(message,"Hi, how are you?")

@bot.message_handler(func=lambda m:True)
def echo_all(message):
    bot.reply_to(message,message.text)

bot.polling()