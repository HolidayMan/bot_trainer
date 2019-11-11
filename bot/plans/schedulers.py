import schedule
from bot.bot import bot, clean_buffer
from core.db import set_state, PlanDB, UserDB, HabbitDB, get_current_state, UserInfoDB
from .description import EN_NAME
from .plan_add_handlers import add_plan
import os

def get_all_users():
    habbitdb = HabbitDB(en_name=EN_NAME)
    return habbitdb.get_all_users()


def remind2plan(users=None, chat_id=None):
    if users:
        for user in users:
            add_plan(chat_id=user.tg_id)
    elif chat_id:
        add_plan(chat_id=chat_id)
        

if os.environ["TEST"] == "false":
    for user in get_all_users():
        userinfo = UserInfoDB(user=user).get_user_info()
        time_string = userinfo.planning_time.strftime('%H:%M:%S')
        schedule.every().day.at(time_string).do(remind2plan, users=(user,))
