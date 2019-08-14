from telebot import types
from bot.bot import bot
from bot.states.plan_states import PlanStates
from bot.states.base_states import States
from core.db import set_state, get_current_state


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_ENTERCOMMAND.value, commands=["my_plans"])
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


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_ENTERCOMMAND.value, commands=["add_plan"])
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
    set_state(message.chat.id, PlanStates.S_NEWCHOOSETYPE.value)
