from bot.bot import bot
from bot.plans.handlers import *
from bot.schedulers import *
import threading
import schedule
import time

def check_schedulers():
    while True:
        schedule.run_pending()
        time.sleep(1)

poll_thread = threading.Thread(target=bot.polling, kwargs={'none_stop': True}, daemon=True)
schedule_thread = threading.Thread(target=check_schedulers, daemon=True)

poll_thread.start()
schedule_thread.start()
poll_thread.join()
