import re
from datetime import date
from telebot import types

from models.project_model import Project
from models.performer_model import Performer
from core.db import set_state, get_current_state, UserDB, ProjectDB, PerformerDB

from bot.bot import bot, clean_buffer
from bot.states.base_states import States
from bot.states.checklist_states import ChecklistStates
from bot.checklist.microlessons import get_lt_from_number
from bot.buffer import Buffer
from core.exceptions import DateParseError
import bot.checklist.phrases as ph

from .commands import *
from .callbacks import *


def parse_date(date_string):
    date_pattern = r"\d{2}\.\d{2}\.\d{2}"
    dates = re.findall(date_pattern, date_string)
    if len(dates) != 2:
        raise DateParseError(f"Date string {date_string}is invalid")
    date1, date2 = [s.split('.') for s in dates]
    date1 = date(*map(int, reversed(date1)))
    date2 = date(*map(int, reversed(date2)))
    return date1, date2


def parse_one_date(date_string):
    date_pattern = r"\d{2}\.\d{2}\.\d{2}"
    dates = re.findall(date_pattern, date_string)
    if len(dates) != 1:
        raise DateParseError(f"Date string {date_string}is invalid")
    date1 = dates[0].split('.')
    date1 = date(*map(int, reversed(date1)))
    return date1


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == ChecklistStates.STATE_MCL_1.value)
def project_name_handler(message: types.Message):
    project_name = message.text
    new_project = Project()
    new_project.name = project_name
    buffer = Buffer()
    buffer_key = str(message.chat.id) + 'new_project'
    buffer.add_or_change(buffer_key, new_project)

    set_state(message.chat.id, ChecklistStates.STATE_MCL_2.value)
    return bot.send_message(message.chat.id, get_lt_from_number(2), parse_mode="markdown")


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == ChecklistStates.STATE_MCL_2.value)
def project_date_handler(message: types.Message):
    try:
        dates = parse_date(message.text)
    except DateParseError:
        return bot.send_message(message.chat.id, ph.INCORRECT_DATE, parse_mode="markdown"),

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


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == ChecklistStates.STATE_MCL_4.value)
def task_name_handler(message):
    new_task = Task(name=message.text)
    buffer = Buffer()
    buffer_key = str(message.chat.id) + "new_task"
    buffer.add_or_change(buffer_key, new_task)
    set_state(message.chat.id, ChecklistStates.STATE_MCL_5.value)
    return bot.send_message(message.chat.id, get_lt_from_number(5), parse_mode="markdown")


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == ChecklistStates.STATE_MCL_5.value)
def task_date_handler(message):
    try:
        date = parse_one_date(message.text)
    except DateParseError:
        return bot.send_message(message.chat.id, ph.INCORRECT_DATE, parse_mode="markdown"),

    buffer = Buffer()
    buffer_key = str(message.chat.id) + "new_task"
    new_task = buffer.get(buffer_key)
    new_task.date_start = date
    buffer.add_or_change(buffer_key, new_task)
    set_state(message.chat.id, ChecklistStates.STATE_MCL_6.value)
    return bot.send_message(message.chat.id, ph.DATE_ADDED), bot.send_message(message.chat.id, get_lt_from_number(6), parse_mode="markdown")


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == ChecklistStates.STATE_MCL_6.value)
def task_duration_handler(message):
    try:
        duration = int(message.text)
    except ValueError:
        return bot.send_message(message.chat.id, ph.INCORRECT_DURATION, parse_mode="markdown"),
    
    buffer = Buffer()
    buffer_key = str(message.chat.id) + "new_task"
    new_task = buffer.get(buffer_key)
    new_task.duration = duration
    curr_project = buffer.get(str(message.chat.id) + "chosen_project")
    new_task.project = curr_project
    userdb = UserDB(message.chat)
    new_task.user = userdb.user
    taskdb = TaskDB(instance=new_task)
    taskdb.create()

    projectdb = ProjectDB(userdb)
    projects = projectdb.get_all_projects()
    ind = projects.index(curr_project)

    set_state(message.chat.id, ChecklistStates.STATE_PROJECT_PAGE.value)
    class MyCall:
        data = 'projectindex_' + str(ind)
    call = MyCall()
    call.message = message
    return (
            bot.send_message(message.chat.id, ph.DURATION_ADDED, parse_mode="markdown"),
            bot.send_message(message.chat.id, get_lt_from_number(7), parse_mode="markdown"),
            choose_project(call, send_new=True)
    )


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == ChecklistStates.STATE_MCL_8.value)
def performer_name_handler(message: types.Message):
    new_performer = Performer(name=message.text)
    buffer = Buffer()
    buffer_key = str(message.chat.id) + "new_performer"
    buffer.add_or_change(buffer_key, new_performer)
    set_state(message.chat.id, ChecklistStates.STATE_MCL_9.value)
    return (
            bot.send_message(message.chat.id, ph.NAME_ADDED, parse_mode="markdown"),
            bot.send_message(message.chat.id, get_lt_from_number(9), parse_mode="markdown"),
    )


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == ChecklistStates.STATE_MCL_9.value)
def performer_phone_handler(message: types.Message):
    if message.text == '.':
        set_state(message.chat.id, ChecklistStates.STATE_MCL_10.value)
    else:
        buffer = Buffer()
        buffer_key = str(message.chat.id) + "new_performer"
        new_performer = buffer.get(buffer_key)
        new_performer.phone_number = message.text
        buffer.add_or_change(buffer_key, new_performer)
        set_state(message.chat.id, ChecklistStates.STATE_MCL_10.value)

    return (
        bot.send_message(message.chat.id, ph.PHONE_ADDED, parse_mode="markdown"),
        bot.send_message(message.chat.id, get_lt_from_number(10), parse_mode="markdown")
    )


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == ChecklistStates.STATE_MCL_10.value)
def performer_comment_handler(message: types.Message):
    buffer = Buffer()
    buffer_key = str(message.chat.id) + "new_performer"
    buffer_task_key = str(message.chat.id) + "chosen_task"
    buffer_project_key = str(message.chat.id) + "chosen_project"
    new_performer = buffer.get(buffer_key)

    userdb = UserDB(message.chat)

    curr_task = buffer.get(buffer_task_key)
    curr_project = buffer.get(buffer_project_key)
    new_performer.comment = message.text
    new_performer.tasks.append(curr_task)
    new_performer.user = userdb.user
    performerdb = PerformerDB(instance=new_performer)
    performerdb.create()

    projectdb = ProjectDB(instance=curr_project)
    taskdb = TaskDB(project=projectdb.project)
    tasks = taskdb.get_all_tasks()
    ind = tasks.index(curr_task)

    class MyCall:
        data = 'taskindex_' + str(ind)
    call = MyCall()
    call.message = message
    return (
        bot.send_message(message.chat.id, ph.COMMENT_ADDED, parse_mode="markdown"),
        choose_task(call, send=True)
    )


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == ChecklistStates.STATE_MCL_11.value)
def task_comment_handler(message: types.Message):
    buffer = Buffer()
    buffer_project_key = str(message.chat.id) + "chosen_project"
    buffer_task_key = str(message.chat.id) + "chosen_task"
    curr_task = buffer.get(buffer_task_key)
    comment = message.text

    taskdb = TaskDB(instance=curr_task)
    taskdb.task.comments = comment
    taskdb.save()

    curr_project = buffer.get(buffer_project_key)

    projectdb = ProjectDB(instance=curr_project)
    task2db = TaskDB(project=projectdb.project)
    tasks = task2db.get_all_tasks()
    ind = tasks.index(taskdb.task)

    class MyCall:
        data = 'taskindex_' + str(ind)
    call = MyCall()
    call.message = message
    return (
        bot.send_message(message.chat.id, ph.COMMENT_ADDED, parse_mode="markdown"),
        choose_task(call, send=True)
    )

