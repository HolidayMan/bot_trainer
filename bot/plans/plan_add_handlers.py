from bot.bot import bot, clean_buffer
from telebot import types
from bot.states.plan_states import PlanStates
from bot.states.base_states import States
from bot.buffer import Buffer
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
    set_state(message.chat.id, PlanStates.S_NEWCHOOSETYPE.value)


@bot.callback_query_handler(func=lambda call: get_current_state(call.message.chat.id) == PlanStates.S_NEWCHOOSETYPE.value)
def choice_type(call):
    UserDB(call.message.chat) # creating user in DB if he doesn't exist
    switch_type = {
        "today": Plan.TYPE_TODAY,
        "tomorrow": Plan.TYPE_DAY,
        "week": Plan.TYPE_WEEK,
        "month": Plan.TYPE_MONTH,
        "year": Plan.TYPE_YEAR
    }[call.data]
    new_plan = Plan(type=switch_type)
    buffer = Buffer()
    buffer.buffer[str(call.message.chat.id)+"plan"] = new_plan
    bot.delete_message(call.message.chat.id, call.message.message_id)
    set_state(call.message.chat.id, PlanStates.S_NEWENTERTITLE.value)
    bot.send_message(call.message.chat.id, "Какое название?")


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == PlanStates.S_NEWENTERTITLE.value)
def enter_title(message):
    user = UserDB(message.chat)
    if len(message.text) > 128:
        bot.send_message(message.chat.id, "Слишком длинное название. Максимальная длина 128 символов. Попробуй снова.")
        return
    buffer = Buffer()
    plan = buffer.buffer[str(message.chat.id)+"plan"]
    plan.title = message.text
    plan.user = user.user
    plan.status = Plan.STATUS_WAIT
    PlanDB(user).create(plan=plan) # connection will be closed here
    clean_buffer(message.chat.id)
    bot.send_message(message.chat.id, f'План "{message.text}" успешно создан!')
    set_state(message.chat.id, States.S_ENTERCOMMAND.value)
    