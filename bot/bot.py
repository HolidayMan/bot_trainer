import telebot
from bot.states.base_states import States
from core.db import UserDB, set_state
from bot.buffer import Buffer
try:
    import local_settings.config as config
except ModuleNotFoundError:
    import prod_settings.config as config


def clean_buffer(user_id):
    if type(user_id) == int:
        user_id = str(user_id)
    buffer = Buffer()
    for key in buffer.buffer.copy().keys():
        if key.startswith(user_id):
            buffer.buffer.pop(key)


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def cmd_start(message):
    HELP_MESSAGE = "It's a bot"
    UserDB(message.chat)
    bot.send_message(message.chat.id, HELP_MESSAGE)


@bot.message_handler(commands=['cancel'])
def cmd_cancel(message):
    set_state(message.chat.id, States.S_ENTERCOMMAND.value)
    bot.send_message(message.chat.id, "Введите команду")


@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel(call):
    set_state(call.message.chat.id, States.S_ENTERCOMMAND.value)
    clean_buffer(call.message.chat.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
