import importlib
import schedule

from core.utils.time import OCLOCK_8
from core.utils.articles import get_random_article
from core.db import UserDB, UserInfoDB
from bot.bot import bot
from bot.phrases import HELLO_PHRASE
try:
    import local_settings.config as config
except ModuleNotFoundError:
    import prod_settings.config as config

[importlib.import_module(f'bot.{habbit}.schedulers', package='*') for habbit in config.HABBITS]


def get_all_users():
    return UserDB.get_all_users()


def morning_tasks(users):
    for user in users:
        try:
            bot.send_message(user.tg_id, text=HELLO_PHRASE % UserInfoDB(user=user).get_user_info().name, parse_mode="markdown")
            bot.send_message(user.tg_id, text=get_random_article(), parse_mode="HTML")
        except:
            pass

OCLOCK_8_STRING = '0%d:00:00' % int(OCLOCK_8.total_seconds() // 3600)
schedule.every().day.at(OCLOCK_8_STRING).do(morning_tasks, get_all_users())
