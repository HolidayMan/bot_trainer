from bot.bot import bot
from telebot import types
from bot.states.checklist_states import ChecklistStates
from bot.states.base_states import States
from core.db import set_state, get_current_state, ProjectDB, UserDB, TaskDB
from bot.checklist.microlessons import get_lt_from_number
from core.utils.paginator import Paginator

def paginate_projects(projects, page=1):
    projects_on_page = 10
    paginator = Paginator(projects, projects_on_page)
    page = paginator.page(page)

    if page.data:
        message_text = f'Ваши проекты: (страница {page.number} из {paginator.last_page_number()})\n'
        for num, project in enumerate(page, page.start_index+1): # generating of a message
            message_text+='{} _{}_\n'.format(num, project.name)
    else:
        return  (f'У вас нет проектов', None)

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
        message_text = f'{project.name}: (страница {page.number} из {paginator.last_page_number()})\n'
        for num, project in enumerate(page, page.start_index+1): # generating of a message
            message_text+='{} _{}_\n'.format(num, project.name)
    else:
        message_text = f'У вас нет задач в проекте {project.name}'

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

    return message_text, keyboard


@bot.message_handler(commands=['add_project'])
def cmd_add_project(message: types.Message):
    set_state(message.chat.id, ChecklistStates.STATE_MCL_1.value)
    return bot.send_message(message.chat.id, get_lt_from_number(1))


@bot.message_handler(commands=['my_projects'])
def cmd_my_projects(message: types.Message):
    set_state(message.chat.id, ChecklistStates.STATE_CHOOSE_PROJECT.value)
    userdb = UserDB(message.chat)
    projects = ProjectDB(user_db_object=userdb)
    projects = projects.get_all_projects()
    message_text, keyboard = paginate_projects(projects)
    return bot.send_message(chat_id=message.chat.id, text=message_text, parse_mode="markdown", reply_markup=keyboard)
