from bot.bot import bot
from telebot import types
from bot.states.checklist_states import ChecklistStates
from bot.states.base_states import States
from core.db import set_state, get_current_state
from bot.checklist.microlessons import get_lt_from_number

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_ENTERCOMMAND.value, commands=['add_project'])
def cmd_add_project(message: types.Message):
    set_state(message.chat.id, ChecklistStates.STATE_MCL_1.value)
    return bot.send_message(message.chat.id, get_lt_from_number(1))
