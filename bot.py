from heapq import merge
import telebot
from telebot import types
import os
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States
from telebot.storage import StateMemoryStorage

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

class MyStates(StatesGroup):
    defualt = State()
    download = State() 
    upload = State()
    attach = State()
state_storage = StateMemoryStorage() # you can init here another storage
with open('token.txt','r') as file:
    token = file.read()
bot = telebot.TeleBot(token,
state_storage=state_storage)



def keyboard(key_type="Normal"):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('download from youtube.')
    itembtn2 = types.KeyboardButton('upload custome subtitle.')
    itembtn3 = types.KeyboardButton('attach video and subtitle.')
    markup.add(itembtn1, itembtn2, itembtn3)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # bot.set_state(message.from_user.id, MyStates.download, message.chat.id)
    bot.send_message(message.chat.id, "hi.choose an option",reply_markup=keyboard())

# Any state
@bot.message_handler(state="*", commands='cancel')
def any_state(message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, "Your state was cancelled.")
    bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(state = MyStates.download)
def yt_dl(message):
    chat_id = message.chat.id
    bot.set_state(message.from_user.id, MyStates.defualt, message.chat.id)
    try:
        bot.send_message(chat_id, "downloading...")
        os.system(f"yt-dlp --format mp4 -o 'yt_file.mp4' --sub-lang fa --write-auto-sub --convert-subs=srt {message.text}")
        bot.reply_to(message, "done!\nuploading")
        with open("yt_file.mp4","rb") as video:
            bot.send_video(chat_id,video)
        with open("yt_file.fa.srt","rb") as sub:
            bot.send_document(chat_id,sub)
    except Exception as e:
        os.system("rm yt_file*")
        bot.reply_to(message, "error occurred!\ntry again in a cupple of seconds")
@bot.message_handler(state = MyStates.upload,content_types=['document'])
def get_sub(message):
    bot.set_state(message.from_user.id, MyStates.defualt, message.chat.id)
    file_path = bot.get_file(message.document.file_id).file_path
    file = bot.download_file(file_path)
    with open("yt_file.fa.srt","wb") as sub:
        sub.write(file)
    bot.send_message(message.chat.id,"done!")
@bot.message_handler(state = MyStates.attach)
def merge(message):
    bot.set_state(message.from_user.id, MyStates.defualt, message.chat.id)
    # if(" " in message):
    #     bot.send_message(message.chat.id,"dont use space in your name!\try again")
    bot.send_message(message.chat.id,"starting")
    os.system(f"ffmpeg -i yt_file.mp4 -vf subtitles=yt_file.fa.srt {message.text}.mp4")
    bot.send_message(message.chat.id,"done!\nuploading")
    with open(f"{message.text}.mp4","rb") as video:
        bot.send_video(message.chat.id,video,timeout=None)

@bot.message_handler(func=lambda message: True)
def all_messages(message):
    if(message.text =='download from youtube.'):
        bot.set_state(message.from_user.id, MyStates.download, message.chat.id)
        bot.send_message(message.chat.id,"send me a youtube url:")
    elif(message.text == 'upload custome subtitle.'):
        bot.set_state(message.from_user.id, MyStates.upload, message.chat.id)
        bot.send_message(message.chat.id,"send me your new subtitle file.")
    elif(message.text == 'attach video and subtitle.'):
        bot.set_state(message.from_user.id, MyStates.attach, message.chat.id)
        bot.send_message(message.chat.id,"enter the name of your video") # add update for keyboard and forwarding files for user to check
    else:
        bot.reply_to(message, "please choose an option",reply_markup=keyboard())

bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.infinity_polling()








# # Any state
# @bot.message_handler(state="*", commands='cancel')
# def any_state(message):
#     """
#     Cancel state
#     """
#     bot.send_message(message.chat.id, "Your state was cancelled.")
#     bot.delete_state(message.from_user.id, message.chat.id)

# @bot.message_handler(state=MyStates.name)
# def name_get(message):
#     """
#     State 1. Will process when user's state is MyStates.name.
#     """
#     bot.send_message(message.chat.id, f'Now write me a surname')
#     bot.set_state(message.from_user.id, MyStates.surname, message.chat.id)
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['name'] = message.text
 
 
# @bot.message_handler(state=MyStates.surname)
# def ask_age(message):
#     """
#     State 2. Will process when user's state is MyStates.surname.
#     """
#     bot.send_message(message.chat.id, "What is your age?")
#     bot.set_state(message.from_user.id, MyStates.age, message.chat.id)
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['surname'] = message.text
 
# # result
# @bot.message_handler(state=MyStates.age, is_digit=True)
# def ready_for_answer(message):
#     """
#     State 3. Will process when user's state is MyStates.age.
#     """
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         bot.send_message(message.chat.id, "Ready, take a look:\n<b>Name: {name}\nSurname: {surname}\nAge: {age}</b>".format(name=data['name'], surname=data['surname'], age=message.text), parse_mode="html")
#     bot.delete_state(message.from_user.id, message.chat.id)

# #incorrect number
# @bot.message_handler(state=MyStates.age, is_digit=False)
# def age_incorrect(message):
#     """
#     Wrong response for MyStates.age
#     """
#     bot.send_message(message.chat.id, 'Looks like you are submitting a string in the field age. Please enter a number')

# # register filters

# bot.add_custom_filter(custom_filters.StateFilter(bot))
# bot.add_custom_filter(custom_filters.IsDigitFilter())

