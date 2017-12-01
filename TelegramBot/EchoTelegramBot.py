import telebot
import config
import BDConn as bd
import re

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.send_message(message.chat.id,"Welcome to SameMulicBot \n To find similar songs use comand /simsong")
@bot.message_handler(commands=['simsong'])
def send_simsong(message):
    bot.send_message(message.chat.id, 'Write Artist of the song and title in format:\nArtist-Title')

@bot.message_handler(func=lambda m:True)
def sim_song_select(message):
    r=message.text
    rep=bd.SelectSimilars(r)
    msg = bot.send_message(message.chat.id, rep)
    #bot.reply_to(message,rep)

bot.polling()