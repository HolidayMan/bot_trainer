from telebot import types
import re

from models.project_model import Project
from core.db import set_state, get_current_state, UserDB, ProjectDB

from bot.bot import bot, clean_buffer
from bot.states.base_states import States
from bot.states.checklist_states import ChecklistStates
from bot.checklist.microlessons import get_lt_from_number
from bot.buffer import Buffer
from core.exceptions import DateParseError


from .commands import *


def parse_date(date_string): #uncompleted
    date_pattern = r"\d{2}:\d{2}:\d{2}"
    dates = re.findall(date_pattern, date_string)
    if len(dates) != 2:
        raise DateParseError(f"Date string {date_string}is invalid")


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == ChecklistStates.STATE_MCL_1.value, types=['text'])
def project_name_handler(message: types.Message):
    project_name = message.text
    new_project = Project()
    new_project.name = project_name
    buffer = Buffer()
    buffer_key = str(message.chat.id) + 'new_project'
    buffer.add_or_change(buffer_key, new_project)
    set_state(message.chat.id, ChecklistStates.STATE_MCL_2.value)
    return bot.send_message(message.chat.id, get_lt_from_number(2))

    # projectdb = ProjectDB(instance=Project)
    # projectdb.create()


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == ChecklistStates.STATE_MCL_2.value, types=['text'])
def project_date_handler(message: types.Message):
    pass
