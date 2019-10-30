import telebot
from bot.states.base_states import States
from bot.questionary.questions import Questionary
from bot.states.questionary_states import QuestionaryStates
from core.db import UserDB, HabbitDB, set_state, UserInfoDB
from bot.buffer import Buffer, clean_buffer
try:
    import local_settings.config as config
except ModuleNotFoundError:
    import prod_settings.config as config


bot = telebot.TeleBot(config.TOKEN)


def clean_buffer(user_id):
    if type(user_id) == int:
        user_id = str(user_id)
    buffer = Buffer()
    for key in buffer.buffer.copy().keys():
        if key.startswith(user_id):
            buffer.buffer.pop(key)


@bot.message_handler(commands=['start'])
def cmd_start(message):
    HELP_MESSAGE = "It's a bot"
    if not message.chat.type == "private":
        bot.send_message(message.chat.id, "I work only in private chats.")
        return
    userdb = UserDB(message.chat)
    habbitdb = HabbitDB(user_db_object=userdb)
    userinfodb = UserInfoDB(userdb_obj=userdb)

    if not userinfodb.get_user_info():
        questionary = Questionary()
        questionary.ask_question(bot, message, questionary.question_1,  QuestionaryStates.S_QUESTION1.value)
    else:
        bot.send_message(message.chat.id, HELP_MESSAGE)

    for habbit_en_name in config.DEFAULT_HABBITS:
        habbitdb.set_habbit(en_name=habbit_en_name)
        try:
            habbitdb.set_user_habbit()
        except ValueError: # if user already has this habbit
            pass


@bot.message_handler(commands=['cancel'])
def cmd_cancel(message):
    set_state(message.chat.id, States.S_ENTERCOMMAND.value)
    bot.send_message(message.chat.id, "Введите команду")


@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel(call):
    set_state(call.message.chat.id, States.S_ENTERCOMMAND.value)
    clean_buffer(call.message.chat.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
