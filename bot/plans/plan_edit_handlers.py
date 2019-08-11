from bot.bot import bot
from telebot import types
from bot.states.plan_states import PlanStates
from bot.states.base_states import States
from bot.plans.plan_buffer import PlanBuffer
from core.db import set_state, PlanDB, UserDB, get_current_state
from models.plan_model import Plan
from core.utils.paginator import Paginator


def paginate_plans(plans, page=1):
    paginator = Paginator(plans, 2)
    page = paginator.page(page)
    message_text = f'Ваши планы: (страница {page.number} из {paginator.last_page_number()})\n'
    for num, plan in enumerate(page, page.start_index+1): # generating of a message
        message_text+='{} _{}_\n'.format(num, plan.title)

    keyboard = types.InlineKeyboardMarkup()
    prev_page_button = types.InlineKeyboardButton(text="⬅️", callback_data="planpage_"+str(page.previous_page_number) if page.has_previous() else 'planpage_1')
    cancel_button = types.InlineKeyboardButton(text="❌", callback_data="cancel")
    next_page_button = types.InlineKeyboardButton(text="➡️", callback_data="planpage_"+str(page.next_page_number) if page.has_next() else "planpage_"+str(paginator.last_page_number()))
    keyboard.add(
        prev_page_button,
        cancel_button,
        next_page_button
    )
    return message_text, keyboard


@bot.message_handler(commands=["my_plans"])
def cmd_my_plans(message):
    keyboard = types.InlineKeyboardMarkup()
    today_button = types.InlineKeyboardButton(text="Сегодня", callback_data="today")
    tomorrow_button = types.InlineKeyboardButton(text="Завтра", callback_data="tomorrow")
    week_button = types.InlineKeyboardButton(text="Неделя", callback_data="week")
    month_button = types.InlineKeyboardButton(text="Месяц", callback_data="month")
    cancel_button = types.InlineKeyboardButton(text="❌", callback_data="cancel")
    year_button = types.InlineKeyboardButton(text="Год", callback_data="year")
    keyboard.add(
                    today_button, 
                    tomorrow_button,
                    week_button,
                    month_button,
                    cancel_button,
                    year_button
                )
    bot.send_message(message.chat.id, "Какие планы вам показать?", reply_markup=keyboard)
    set_state(message.chat.id, PlanStates.S_EDITCHOOSETYPE.value)


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == PlanStates.S_EDITCHOOSETYPE.value)
def edit_show_plans(call):
    user = UserDB(call.message.chat)
    switch_type = {
        "today": Plan.TYPE_TODAY,
        "tomorrow": Plan.TYPE_DAY,
        "week": Plan.TYPE_WEEK,
        "month": Plan.TYPE_MONTH,
        "year": Plan.TYPE_YEAR
    }[call.data]
    plan_buffer = PlanBuffer()
    plan_buffer.buffer[call.message.chat.username+"editplanstype"] = switch_type
    plan_buffer.buffer[call.message.chat.username+"currentplanpage"] = 1
    plandb = PlanDB(user_db_object=user)
    plans = plandb.get_all_plans(type=switch_type)
    
    message_text, keyboard = paginate_plans(plans)
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, message_text, parse_mode="markdown", reply_markup=keyboard)
    set_state(call.message.chat.id, PlanStates.S_EDITCHOOSEPLAN.value)
    

@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == PlanStates.S_EDITCHOOSEPLAN.value and call.data.split('_')[0] == "planpage")
def edit_paginate(call):
    page_num = int(call.data.split('_')[1])
    plan_buffer = PlanBuffer()
    curr_page_num = plan_buffer.buffer[call.message.chat.username+"currentplanpage"]
    plan_buffer.buffer[call.message.chat.username+"currentplanpage"] = page_num
    print(curr_page_num)
    if page_num == curr_page_num:
        return
    user = UserDB(call.message.chat)
    plan_type = plan_buffer.buffer[call.message.chat.username+"editplanstype"]
    plandb = PlanDB(user_db_object=user)
    plans = plandb.get_all_plans(type=plan_type)
    message_text, keyboard = paginate_plans(plans, page_num)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, parse_mode="markdown", reply_markup=keyboard)