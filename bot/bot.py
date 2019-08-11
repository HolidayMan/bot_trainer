import telebot
from bot.states.base_states import States
from core.db import UserDB, set_state
try:
    import local_settings.config as config
except ModuleNotFoundError:
    import prod_settings.config as config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def cmd_start(message):
    HELP_MESSAGE = "It's a bot"
    UserDB(message.chat)
    bot.send_message(message.chat.id, HELP_MESSAGE)


@bot.message_handler(commands=['cancel'])
def cmd_cancel(message):
    set_state(message.chat.id, States.S_ENTERCOMMAND.value)


@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel(call):
    set_state(call.message.chat.id, States.S_ENTERCOMMAND.value)
    bot.delete_message(call.message.chat.id, call.message.message_id)