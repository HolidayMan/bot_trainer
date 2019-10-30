import re

from bot.bot import bot, clean_buffer
from bot.buffer import Buffer
from datetime import time
from telebot import types
from bot.states.base_states import States
from bot.states.questionary_states import QuestionaryStates
from core.db import set_state, get_current_state, UserDB, UserInfoDB
from models.user_info_model import UserInfo
from .questions import Questionary
from .phrases import *


questionary = Questionary()

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == QuestionaryStates.S_QUESTION1.value)
def handle_answer_1(message) -> tuple:
    chat_id = message.chat.id
    if message.text == None:
        message.text = ''
    name_pattern = r"^([a-zA-Z]|[а-яА-Я]| )+$"
    if re.match(name_pattern, message.text):
        userinfo = UserInfo()
        userinfo.name = message.text
        buffer = Buffer()
        buffer.add_or_change(str(chat_id)+"questionary", userinfo)
        
        return bot.send_message(chat_id=chat_id, text=GREAT), questionary.ask_question(bot_instance=bot, message=message, question=questionary.question_2, state=QuestionaryStates.S_QUESTION2.value)
    else:
        return (bot.send_message(chat_id=chat_id, text=PHRASE_NAME_MUST_CONTAIN_JUST_LETTERS), )


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == QuestionaryStates.S_QUESTION2.value)
def handle_answer_2(message):
    chat_id = message.chat.id
    if message.text == None:
        message.text = ''
    surname_pattern = r"^([a-zA-Z]|[а-яА-Я]| )+$"
    if re.match(surname_pattern, message.text):
        buffer_key = str(chat_id)+"questionary"
        buffer = Buffer()
        userinfo = buffer.buffer.get(buffer_key)
        userinfo.surname = message.text
        buffer.add_or_change(str(chat_id)+"questionary", userinfo)
        
        

        return bot.send_message(chat_id=chat_id, text=GREAT), questionary.ask_question(bot_instance=bot, message=message, question=questionary.question_3, state=QuestionaryStates.S_QUESTION3.value)
    else:
        return bot.send_message(chat_id=chat_id, text=PHRASE_SURNAME_MUST_CONTAIN_JUST_LETTERS),


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == QuestionaryStates.S_QUESTION3.value)
def handle_answer_3(message):
    chat_id = message.chat.id
    try:
        age = int(message.text)
    except ValueError:
        bot.send_message(chat_id=chat_id, text=AGE_MUST_BE_A_NUMBER_AND_BETWEEN)
        return
    if 1 <= age <= 100:
        buffer_key = str(chat_id)+"questionary"
        buffer = Buffer()
        userinfo = buffer.buffer.get(buffer_key)
        userinfo.age = age
        buffer.add_or_change(str(chat_id)+"questionary", userinfo)
        
        bot.send_message(chat_id=chat_id, text=GREAT)

        questionary.ask_question(bot_instance=bot, message=message, question=questionary.question_4, state=QuestionaryStates.S_QUESTION4.value)
    else:
        bot.send_message(chat_id=chat_id, text=AGE_MUST_BE_A_NUMBER_AND_BETWEEN)


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == QuestionaryStates.S_QUESTION4.value) # must be edited for working with time
def handle_answer_4(message):
    chat_id = message.chat.id
    if True: # here will be validating for time
        buffer_key = str(chat_id)+"questionary"
        buffer = Buffer()
        userinfo = buffer.buffer.get(buffer_key)
        userinfo.planning_time = time(19, 00, 00)
        buffer.add_or_change(str(chat_id)+"questionary", userinfo)
        
        bot.send_message(chat_id=chat_id, text=GREAT)

        questionary.ask_question(bot_instance=bot, message=message, question=questionary.question_5, state=QuestionaryStates.S_QUESTION5.value)
    else:
        bot.send_message(chat_id=chat_id, text=AGE_MUST_BE_A_NUMBER_AND_BETWEEN)


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == QuestionaryStates.S_QUESTION5.value) # must be edited for working with time
def handle_answer_5(message):
    chat_id = message.chat.id
    if True: # here will be validating
        buffer_key = str(chat_id)+"questionary"
        buffer = Buffer()
        userinfo = buffer.buffer.get(buffer_key)
        userinfo.question1 = message.text
        buffer.add_or_change(str(chat_id)+"questionary", userinfo)
        
        bot.send_message(chat_id=chat_id, text=GREAT)

        questionary.ask_question(bot_instance=bot, message=message, question=questionary.question_6, state=QuestionaryStates.S_QUESTION6.value)
    else:
        bot.send_message(chat_id=chat_id, text=AGE_MUST_BE_A_NUMBER_AND_BETWEEN)


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == QuestionaryStates.S_QUESTION6.value) # must be edited for working with time
def handle_answer_6(message):
    chat_id = message.chat.id
    if True: # here will be validating
        buffer_key = str(chat_id)+"questionary"
        buffer = Buffer()
        userinfo = buffer.buffer.get(buffer_key)
        userinfo.question2 = message.text
        buffer.add_or_change(str(chat_id)+"questionary", userinfo)
        
        bot.send_message(chat_id=chat_id, text=GREAT)

        questionary.ask_question(bot_instance=bot, message=message, question=questionary.question_7, state=QuestionaryStates.S_QUESTION7.value)
    else:
        bot.send_message(chat_id=chat_id, text=AGE_MUST_BE_A_NUMBER_AND_BETWEEN)


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == QuestionaryStates.S_QUESTION7.value) # must be edited for working with time
def handle_answer_7(message):
    chat_id = message.chat.id
    if True: # here will be validating
        buffer_key = str(chat_id)+"questionary"
        buffer = Buffer()
        userinfo = buffer.buffer.get(buffer_key)
        userinfo.question3 = message.text
        buffer.add_or_change(str(chat_id)+"questionary", userinfo)
        
        bot.send_message(chat_id=chat_id, text=GREAT)

        questionary.ask_question(bot_instance=bot, message=message, question=questionary.question_8, state=QuestionaryStates.S_QUESTION8.value)
    else:
        bot.send_message(chat_id=chat_id, text=AGE_MUST_BE_A_NUMBER_AND_BETWEEN)


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == QuestionaryStates.S_QUESTION8.value) # must be edited for working with time
def handle_answer8(message):
    chat_id = message.chat.id
    if True: # here will be validating
        buffer_key = str(chat_id)+"questionary"
        buffer = Buffer()
        userinfo = buffer.buffer.get(buffer_key)
        userinfo.question4 = message.text

        userdb = UserDB(message.chat)
        userinfo.user = userdb.user

        userinfodb = UserInfoDB(userdb_obj=userdb, user_info_obj=userinfo)
        userinfodb.save()
        clean_buffer(chat_id)
        
        bot.send_message(chat_id=chat_id, text=END_OF_QUESTIONARY)

        set_state(chat_id, States.S_ENTERCOMMAND)

    else:
        bot.send_message(chat_id=chat_id, text=AGE_MUST_BE_A_NUMBER_AND_BETWEEN)
