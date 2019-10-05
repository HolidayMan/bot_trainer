import schedule
from bot.bot import bot, clean_buffer
from core.db import set_state, PlanDB, UserDB, HabbitDB, get_current_state
from .description import EN_NAME
from .plan_add_handlers import add_plan


def get_all_users():
    habbitdb = HabbitDB(en_name=EN_NAME)
    return habbitdb.get_all_users()


def remind2plan(users):
    for user in users:
        add_plan(chat_id=user.tg_id)

schedule.every().day.at('21:09:00').do(remind2plan, users=get_all_users())
