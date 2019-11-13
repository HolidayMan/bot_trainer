import telebot

from bot.buffer import Buffer, clean_buffer
from bot.questionary.questions import Questionary
from bot.states.base_states import States
from bot.states.questionary_states import QuestionaryStates
from core.db import HabbitDB, UserDB, UserInfoDB, get_current_state, set_state

try:
    import local_settings.config as config
except ModuleNotFoundError:
    import prod_settings.config as config


bot = telebot.TeleBot(config.TOKEN)


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
    if get_current_state(message.chat.id) in [state.value for state in QuestionaryStates]:
        bot.send_message(message.chat.id, "Закончите анкетирование.")
    else:
        set_state(message.chat.id, States.S_ENTERCOMMAND.value)
        bot.send_message(message.chat.id, "Введите команду")


@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel(call):
    set_state(call.message.chat.id, States.S_ENTERCOMMAND.value)
    clean_buffer(call.message.chat.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)
