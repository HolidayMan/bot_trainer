from telebot import types
from bot.bot import bot
from datetime import date
import re

from bot.states.checklist_states import ChecklistStates
from bot.states.base_states import States
from core.db import set_state, get_current_state, ProjectDB, UserDB, TaskDB
from bot.checklist.microlessons import get_lt_from_number
from bot.buffer import Buffer
from core.utils.paginator import Paginator
from models.task_model import Task
from core.exceptions import DateParseError
from .generate_diagram import generate_diagram

# def parse_date(date_string):
#     date_pattern = r"\d{2}\.\d{2}\.\d{2}"
#     dates = re.findall(date_pattern, date_string)
#     if len(dates) != 1:
#         raise DateParseError(f"Date string {date_string}is invalid")
#     date1 = dates[0].split('.')
#     date1 = date(*map(int, reversed(date1)))
#     return date1


def paginate_projects(projects, page=1):
    projects_on_page = 10
    paginator = Paginator(projects, projects_on_page)
    page = paginator.page(page)

    if page.data:
        message_text = f'Ваші проекти: (сторінка {page.number} з {paginator.last_page_number()})\n'
        for num, project in enumerate(page, page.start_index+1): # generating of a message
            message_text+='{} _{}_\n'.format(num, project.name)
    else:
        return  (f'У вас немає проектів', None)

    keyboard = types.InlineKeyboardMarkup()

    first_row = []
    second_row = []
    for num, i in enumerate(page.get_range()):
        if num < projects_on_page // 2:
            first_row.append(types.InlineKeyboardButton(text=str(i+1), callback_data="projectindex_"+str(i)))
        else:
            second_row.append(types.InlineKeyboardButton(text=str(i+1), callback_data="projectindex_"+str(i)))
    
    keyboard.row(*first_row)
    keyboard.row(*second_row)
    prev_page_button = types.InlineKeyboardButton(text="⬅️", callback_data="projectpage_"+str(page.previous_page_number) if page.has_previous() else 'projectpage_1')
    cancel_button = types.InlineKeyboardButton(text="❌", callback_data="cancel")
    next_page_button = types.InlineKeyboardButton(text="➡️", callback_data="projectpage_"+str(page.next_page_number) if page.has_next() else "projectpage_"+str(paginator.last_page_number()))

    keyboard.row(
        prev_page_button,
        cancel_button,
        next_page_button
    )

    return message_text, keyboard


def paginate_tasks(project, tasks, page=1):
    tasks_on_page = 10
    paginator = Paginator(tasks, tasks_on_page)
    page = paginator.page(page)

    if page.data:
        message_text = f'{project.name}: (сторінка {page.number} з {paginator.last_page_number()})\n'
        for num, project in enumerate(page, page.start_index+1): # generating of a message
            message_text+='{} _{}_\n'.format(num, project.name)
    else:
        message_text = f'У вас немає задач у проекті {project.name}'

    keyboard = types.InlineKeyboardMarkup()

    first_row = []
    second_row = []
    for num, i in enumerate(page.get_range()):
        if num < tasks_on_page // 2:
            first_row.append(types.InlineKeyboardButton(text=str(i+1), callback_data="taskindex_"+str(i)))
        else:
            second_row.append(types.InlineKeyboardButton(text=str(i+1), callback_data="taskindex_"+str(i)))
    
    keyboard.row(*first_row)
    keyboard.row(*second_row)

    mark_done_button = types.InlineKeyboardButton(text="✅", callback_data="project_mark_done")
    add_task_button = types.InlineKeyboardButton(text='+', callback_data='add_task')
    go_back_button = types.InlineKeyboardButton(text="️🔙", callback_data="projects_go_back")

    keyboard.row(
            mark_done_button,
            add_task_button,
            go_back_button,
    )

    prev_page_button = types.InlineKeyboardButton(text="⬅️", callback_data="taskpage_"+str(page.previous_page_number) if page.has_previous() else 'taskpage_1')
    cancel_button = types.InlineKeyboardButton(text="❌", callback_data="cancel")
    next_page_button = types.InlineKeyboardButton(text="➡️", callback_data="taskpage_"+str(page.next_page_number) if page.has_next() else "taskpage_"+str(paginator.last_page_number()))
    
    keyboard.row(
        prev_page_button,
        cancel_button,
        next_page_button
    )

    keyboard.row(types.InlineKeyboardButton(text="📊", callback_data="generate_diagram"))

    return message_text, keyboard


def gen_task_message(task):
    keyboard = types.InlineKeyboardMarkup()

    add_performer_button = types.InlineKeyboardButton(text="+", callback_data="add_performer")
    comment_button = types.InlineKeyboardButton(text="📝", callback_data="task_comment")
    cancel_button = types.InlineKeyboardButton(text="❌", callback_data="cancel")
    go_back_button = types.InlineKeyboardButton(text="️🔙", callback_data="project_task_go_back")

    keyboard.row(
        add_performer_button,
        comment_button,
        cancel_button,
        go_back_button,
    )

    message_text = f'*{task.name}:*\n'
    if task.performers:
        message_text += "Виконавці:\n"
        for ind, performer in enumerate(task.performers, start=1):
            message_text += f"{ind}. {performer.name}\n"
    else:
        message_text += "Додай виконавців на кнопку +\n"
    message_text += '\n\n'
    if task.comments:
        message_text += "Комментар:\n"
        message_text += f"_{task.comments}_\n"
    else:
        message_text += "Додайте комментар на кнопку 📝" + '\n'

    return message_text, keyboard


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == ChecklistStates.STATE_CHOOSE_PROJECT.value and call.data.split('_')[0] == "projectpage")
def callback_paginate_projects(call):
    next_page_num = int(call.data.split('_')[1])
    userdb = UserDB(call.message.chat)
    projects = ProjectDB(user_db_object=userdb)
    projects = projects.get_all_projects()
    message_text, keyboard = paginate_projects(projects, page=next_page_num)
    return bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, parse_mode="markdown", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == ChecklistStates.STATE_CHOOSE_PROJECT.value and call.data.split('_')[0] == 'projectindex')
def choose_project(call: types.CallbackQuery, send_new=False):
    project_index = int(call.data.split('_')[1])
    userdb = UserDB(call.message.chat)
    projects = ProjectDB(user_db_object=userdb)
    projects = projects.get_all_projects()
    project = projects[project_index]
    projectdb = ProjectDB(instance=project) # to get project from DB
    taskdb = TaskDB(project=projectdb.project)

    message_text, keyboard = paginate_tasks(projectdb.project, taskdb.get_all_tasks())
    set_state(call.message.chat.id, ChecklistStates.STATE_PROJECT_PAGE.value)
    buffer = Buffer()
    buffer_key = str(call.message.chat.id) + "chosen_project"
    buffer.add_or_change(buffer_key, project)
    if send_new:
        return bot.send_message(chat_id=call.message.chat.id, text=message_text, parse_mode="markdown", reply_markup=keyboard)
    else:
        return bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, parse_mode="markdown", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == ChecklistStates.STATE_PROJECT_PAGE.value and call.data == 'projects_go_back')
def projects_go_back(call):
    call.data = "projectpage_1"
    set_state(call.message.chat.id, ChecklistStates.STATE_CHOOSE_PROJECT.value)
    callback_paginate_projects(call)


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == ChecklistStates.STATE_PROJECT_PAGE.value and call.data == 'add_task')
def callback_add_task(call):
    message: types.Message = call.message
    set_state(message.chat.id, ChecklistStates.STATE_MCL_4.value)
    bot.delete_message(message.chat.id, message.message_id)
    return bot.send_message(message.chat.id, get_lt_from_number(4), parse_mode="markdown")


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == ChecklistStates.STATE_PROJECT_PAGE.value and call.data.split("_")[0] == 'taskindex')
def choose_task(call, send=False):
    ind = int(call.data.split("_")[1])
    buffer = Buffer()
    buffer_key = str(call.message.chat.id) + "chosen_project"
    curr_project = buffer.get(buffer_key)
    projectdb = ProjectDB(instance=curr_project) # to get project from DB
    taskdb = TaskDB(project=projectdb.project)
    tasks = taskdb.get_all_tasks()
    task = tasks[ind]
    
    buffer_task_key = str(call.message.chat.id) + "chosen_task"
    buffer.add_or_change(buffer_task_key, task)
    
    message_text, keyboard = gen_task_message(task)

    set_state(call.message.chat.id, ChecklistStates.STATE_TASK_PAGE.value)
    if send:
        return bot.send_message(chat_id=call.message.chat.id, text=message_text, parse_mode="markdown", reply_markup=keyboard)
    else:
        return bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, parse_mode="markdown", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == ChecklistStates.STATE_PROJECT_PAGE.value and call.data.split('_')[0] == "taskpage")
def project_page_paginate(call):
    next_page_num = int(call.data.split('_')[1])
    curr_project = Buffer().get(str(call.message.chat.id) + "chosen_project")
    taskdb = TaskDB(project=curr_project)
    tasks = taskdb.get_all_tasks()
    message_text, keyboard = paginate_tasks(curr_project, tasks, page=next_page_num)
    return bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, parse_mode="markdown", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == ChecklistStates.STATE_TASK_PAGE.value and call.data == 'task_comment')
def task_add_comment(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    set_state(call.message.chat.id, ChecklistStates.STATE_MCL_11.value)
    return bot.send_message(call.message.chat.id, get_lt_from_number(11), parse_mode="markdown")


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == ChecklistStates.STATE_TASK_PAGE.value and call.data == 'project_task_go_back')
def tasks_go_back(call):
    userdb = UserDB(call.message.chat)
    projectdb = ProjectDB(user_db_object=userdb)
    projects = projectdb.get_all_projects()
    buffer = Buffer()
    buffer_key = str(call.message.chat.id) + "chosen_project"
    ind = projects.index(buffer.get(buffer_key))
    call.data = "projectindex_" + str(ind)
    set_state(call.message.chat.id, ChecklistStates.STATE_PROJECT_PAGE.value)
    return choose_project(call)


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == ChecklistStates.STATE_TASK_PAGE.value and call.data == 'add_performer')
def callback_add_performer(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    set_state(call.message.chat.id, ChecklistStates.STATE_MCL_8.value)
    return bot.send_message(call.message.chat.id, get_lt_from_number(8),  parse_mode="markdown")


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == ChecklistStates.STATE_PROJECT_PAGE.value and call.data == 'generate_diagram')
def callback_generate_diagram(call):
    buffer = Buffer()
    project = buffer.get(str(call.message.chat.id) + "chosen_project")
    projectdb = ProjectDB(instance=project)
    try:
        filename = generate_diagram(projectdb.project)
        with open(filename, 'rb') as f:
            bot.send_photo(call.message.chat.id, f)
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, 'Додайте задачі для проекту',  parse_mode="markdown",)
