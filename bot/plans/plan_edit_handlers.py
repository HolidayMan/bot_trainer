from bot.bot import bot
from telebot import types
from bot.states.plan_states import PlanStates
from bot.states.base_states import States
from bot.buffer import Buffer, clean_buffer
from core.db import set_state, PlanDB, UserDB, get_current_state
from models.plan_model import Plan
from core.utils.paginator import Paginator


SWITCH_STATUS = {
    Plan.STATUS_WAIT: "⏱",
    Plan.STATUS_OVERDUE: "❗️",
    Plan.STATUS_CANCELED: "🚫",
    Plan.STATUS_DONE: "✅"
}


def paginate_plans(plans, type, page=1,):
    plans_on_page = 10
    paginator = Paginator(plans, plans_on_page)
    page = paginator.page(page)
    switch_type = {
        Plan.TYPE_TODAY: "сегодня",
        Plan.TYPE_DAY: "завтра",
        Plan.TYPE_WEEK: "неделю",
        Plan.TYPE_MONTH: "месяц",
        Plan.TYPE_YEAR: "год"
    }[type]
    
    if page.data:
        message_text = f'Ваши планы на {switch_type}: (страница {page.number} из {paginator.last_page_number()})\n'
        for num, plan in enumerate(page, page.start_index+1): # generating of a message
            message_text+='{} _{}_ {}\n'.format(num, plan.title, SWITCH_STATUS[plan.status])
    else:
        return  (f'У вас нет планов на {switch_type}', None)

    keyboard = types.InlineKeyboardMarkup()
    
    first_row = []
    second_row = []
    for num, i in enumerate(page.get_range()):
        if num < plans_on_page // 2:
            first_row.append(types.InlineKeyboardButton(text=str(i+1), callback_data="planindex_"+str(i)))
        else:
            second_row.append(types.InlineKeyboardButton(text=str(i+1), callback_data="planindex_"+str(i)))
    keyboard.row(*first_row)
    keyboard.row(*second_row)
    prev_page_button = types.InlineKeyboardButton(text="⬅️", callback_data="planpage_"+str(page.previous_page_number) if page.has_previous() else 'planpage_1')
    cancel_button = types.InlineKeyboardButton(text="❌", callback_data="cancel")
    next_page_button = types.InlineKeyboardButton(text="➡️", callback_data="planpage_"+str(page.next_page_number) if page.has_next() else "planpage_"+str(paginator.last_page_number()))
    keyboard.row(
        prev_page_button,
        cancel_button,
        next_page_button
    )
    return message_text, keyboard


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
    buffer = Buffer()
    buffer.buffer[str(call.message.chat.id)+"currentplanpage"] = 1
    buffer.buffer[str(call.message.chat.id)+"planstype"] = switch_type
    plandb = PlanDB(user_db_object=user)
    plans = plandb.get_all_plans(type=switch_type)
    buffer.buffer[str(call.message.chat.id)+"editplanslist"] = plans
    message_text, keyboard = paginate_plans(plans, switch_type)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, parse_mode="markdown", reply_markup=keyboard)
    set_state(call.message.chat.id, PlanStates.S_EDITCHOOSEPLAN.value)
    

@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == PlanStates.S_EDITCHOOSEPLAN.value and call.data.split('_')[0] == "planpage")
def edit_paginate(call):
    next_page_num = int(call.data.split('_')[1])
    buffer = Buffer()
    curr_page_num = buffer.buffer[str(call.message.chat.id)+"currentplanpage"]
    plans = buffer.buffer[str(call.message.chat.id)+"editplanslist"]
    message_text, keyboard = paginate_plans(plans, plans[0].type, next_page_num)
    buffer.buffer[str(call.message.chat.id)+"currentplanpage"] = next_page_num
    if curr_page_num != next_page_num or call.data.split('_')[0] == 'goback': # checking if user came back from choosed plan
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, parse_mode="markdown", reply_markup=keyboard)

    
    

@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == PlanStates.S_EDITCHOOSEPLAN.value and call.data.split('_')[0] == 'planindex')
def edit_plan(call):
    plan_index = int(call.data.split('_')[1])
    buffer = Buffer()
    plan = buffer.buffer[str(call.message.chat.id)+"editplanslist"][plan_index] # get a plan instance
    buffer.buffer[str(call.message.chat.id)+"editchosenplan"] = plan
    message_text = f"Что сделать?\n {plan_index+1} _{plan.title}_ {SWITCH_STATUS[plan.status]}"
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    mark_done_button = types.InlineKeyboardButton(text="✅", callback_data="plan_mark_done")
    mark_canceled_button = types.InlineKeyboardButton(text="🚫", callback_data="plan_mark_canceled")
    go_back_button = types.InlineKeyboardButton(text="️🔙", callback_data="go_back")
    cancel_button = types.InlineKeyboardButton(text="❌", callback_data="cancel")
    keyboard.add(
            mark_done_button, 
            mark_canceled_button,
            go_back_button,
            cancel_button
        )
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text, parse_mode="markdown", reply_markup=keyboard)
    set_state(call.message.chat.id, PlanStates.S_EDITPLAN.value)


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == PlanStates.S_EDITPLAN.value and call.data == "go_back")
def edit_go_back(call):
    buffer = Buffer()

    call.data = 'goback_'+str(buffer.buffer[str(call.message.chat.id)+"currentplanpage"])
    set_state(call.message.chat.id, PlanStates.S_EDITCHOOSEPLAN.value)
    edit_paginate(call)


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == PlanStates.S_EDITPLAN.value and call.data == "plan_mark_done")
def edit_plan_mark_done(call):
    buffer = Buffer()
    plan = buffer.buffer[str(call.message.chat.id)+"editchosenplan"]
    userdb = UserDB(call.message.chat)
    plandb = PlanDB(user_db_object=userdb, instance=plan)
    plandb.mark_done()
    plans = plandb.get_all_plans(type=buffer.buffer[str(call.message.chat.id)+"planstype"])
    buffer.buffer[str(call.message.chat.id)+"editplanslist"] = plans
    buffer.save()
    edit_go_back(call)


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == PlanStates.S_EDITPLAN.value and call.data == "plan_mark_canceled")
def edit_plan_mark_cancel(call):
    buffer = Buffer()
    plan = buffer.buffer[str(call.message.chat.id)+"editchosenplan"]
    userdb = UserDB(call.message.chat)
    plandb = PlanDB(user_db_object=userdb, instance=plan)
    plandb.mark_canceled()
    plans = plandb.get_all_plans(type=buffer.buffer[str(call.message.chat.id)+"planstype"])
    buffer.buffer[str(call.message.chat.id)+"editplanslist"] = plans
    buffer.save()
    edit_go_back(call)

