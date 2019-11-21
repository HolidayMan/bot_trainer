import re
from datetime import date
from telebot import types

from models.project_model import Project
from core.db import set_state, get_current_state, UserDB, ProjectDB

from bot.bot import bot, clean_buffer
from bot.states.base_states import States
from bot.states.checklist_states import ChecklistStates
from bot.checklist.microlessons import get_lt_from_number
from bot.buffer import Buffer
from core.exceptions import DateParseError
import bot.checklist.phrases as ph

from .commands import *


def parse_date(date_string):
    date_pattern = r"\d{2}\.\d{2}\.\d{2}"
    dates = re.findall(date_pattern, date_string)
    if len(dates) != 2:
        raise DateParseError(f"Date string {date_string}is invalid")
    date1, date2 = [s.split('.') for s in dates]
    date1 = date(*map(int, reversed(date1)))
    date2 = date(*map(int, reversed(date2)))
    return date1, date2


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == ChecklistStates.STATE_MCL_1.value)
def project_name_handler(message: types.Message):
    project_name = message.text
    new_project = Project()
    new_project.name = project_name
    buffer = Buffer()
    buffer_key = str(message.chat.id) + 'new_project'
    buffer.add_or_change(buffer_key, new_project)

    set_state(message.chat.id, ChecklistStates.STATE_MCL_2.value)
    return bot.send_message(message.chat.id, get_lt_from_number(2))


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == ChecklistStates.STATE_MCL_2.value)
def project_date_handler(message: types.Message):
    try:
        dates = parse_date(message.text)
    except DateParseError:
        return bot.send_message(message.chat.id, ph.INCORRECT_DATE),

    buffer = Buffer()
    buffer_key = str(message.chat.id) + 'new_project'
    project = buffer.get(buffer_key)
    
    userdb = UserDB(message.chat)
    project.date_start = dates[0]
    project.date_end = dates[1]
    project.user = userdb.user
    projectdb = ProjectDB(instance=project)
    projectdb.create()

    set_state(message.chat.id, States.S_ENTERCOMMAND.value)
    return bot.send_message(message.chat.id, ph.PROJECT_ADDED), bot.send_message(message.chat.id, get_lt_from_number(3))

