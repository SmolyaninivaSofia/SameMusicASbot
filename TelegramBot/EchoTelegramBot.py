import telebot
import config
import BDConn as bd
import re

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.send_message(message.chat.id,"Welcome to SameMulicBot \n To find similar songs write \'Iwant Artist-Title\'")
#@bot.message_handler(commands=['simsong'])
#def send_simsong(message):
#    bot.send_message(message.chat.id, 'Write Artist of the song and title in format:\nArtist-Title')

@bot.message_handler(func=lambda m:True)
def sim_song_select(message):
    r=message.text
    b=r[0:r.find(' ')]
    rep=''
    if b=='Iwant':
        r=r[r.find(' ')+1:len(r)]
        res=bd.SelectSimilars(r)
        if (res!=''):
            rep+='List of songs similar to '+r.upper()+'\n'+res
        else:
            rep += 'Sorry...This song have no similars :( \nOr you can make a mistake. Check that you write song and title in format:\nArtist-Title\n\nAlso you can add your song to the bot. For this you shold write \nAdd Artist-Title:tag1,tag2\n(the count of tags may be different)'
    elif b=='Add':
        r = r[r.find(' ') + 1:len(r)]
        res=bd.Add(message.chat.id,r)
        if res==1:
            rep += 'Song addition is failed. Please, check the input format and try again. Input format must be:\nArtist-Title:tag1,tag2\n(the count of tags may be different)'
        elif res==2:
            rep += 'Song addition is failed. You can\'t add one song more than 1 times.'
        elif res==0:
            rep += 'Song successfully added to the sandbox. It will appear at the bot answers in a few days.'
    else:
        rep +='It is a to SameMulicBot \nTo find similar songs write:\nIwant Artist-Title'
    bot.send_message(message.chat.id, rep)

bot.polling()