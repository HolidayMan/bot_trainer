from bot.bot import bot
from telebot import types
from bot.states.plan_states import PlanStates
from bot.plans.plan_buffer import PlanBuffer
from core.db import set_state, PlanDB, UserDB, get_current_state
from models.plan_model import Plan

@bot.message_handler(commands=["add_plan"])
def add_plan(message):
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
    bot.send_message(message.chat.id, "На когда план?", reply_markup=keyboard)
    set_state(message.chat.id, PlanStates.S_CHOOSETYPE.value)


@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def cancel(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == PlanStates.S_CHOOSETYPE.value)
def choice_type(call):
    user = UserDB(call.message.chat)
    switch_type = {
        "today": Plan.TYPE_TODAY,
        "tomorrow": Plan.TYPE_DAY,
        "week": Plan.TYPE_WEEK,
        "month": Plan.TYPE_MONTH,
        "year": Plan.TYPE_YEAR
    }[call.data]
    new_plan = Plan(type=switch_type)
    plan_buffer = PlanBuffer()
    plan_buffer.buffer[call.message.chat.username+"plan"] = new_plan
    plan_buffer.save()
    bot.delete_message(call.message.chat.id, call.message.message_id)


