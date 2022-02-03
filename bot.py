import telebot
from telebot import types
import os
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States
from telebot.storage import StateMemoryStorage

from telebot.types import ReplyKeyboardMarkup, KeyboardButton
# with open('token.txt','r') as file:
#     token = file.read()

# bot = telebot.TeleBot(token, parse_mode=None)

# keys = ["1","2","3","4","5","6","7","8","9","0","q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"]
# symbols = ["1","2","3","4","5","6","7","8","9","0","!","@","#","$","%","^","&","*","(",")","\'","\"","/","\\",",",".",";",":"]

# def keyboard(key_type="Normal"):
#     markup = types.ReplyKeyboardMarkup(row_width=2)
#     itembtn1 = types.KeyboardButton('download from youtube.')
#     itembtn2 = types.KeyboardButton('upload custome subtitle.')
#     itembtn3 = types.KeyboardButton('attach video and subtitle.')
#     markup.add(itembtn1, itembtn2, itembtn3)
#     return markup

# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     chat_id = message.chat.id
#     bot.reply_to(message, "hi",reply_markup=keyboard())

# @bot.message_handler(func=lambda message: True)
# def yt_dl(message):
#     try:
#         os.system(f"yt-dlp --format mp4 -o 'yt_file.mp4' --sub-lang fa --write-auto-sub --convert-subs=srt {message.text}")
#         bot.reply_to(message, message.text)
#     except Exception as e:
#         os.system("rm yt_file*")
#         bot.reply_to(message, "error occurred!\ntry again in a cupple of seconds")



# bot.infinity_polling()

