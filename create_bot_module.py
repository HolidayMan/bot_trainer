import os, sys

BASE_DIR = os.path.dirname(__file__)

module_name = sys.argv[1]
module_dir = os.path.join(BASE_DIR, 'bot', module_name)
os.mkdir(module_dir)

with open(os.path.join(module_dir, 'handlers.py'), 'w') as file:
    file.write("""from bot.bot import bot, clean_buffer
from telebot import types
from bot.states.base_states import States
from core.db import set_state, get_current_state, PlanDB, UserDB
""")


with open(os.path.join(module_dir, '__init__.py'), 'w'):
    pass


with open(os.path.join(module_dir, 'description.py'), 'w'):
    pass


with open(os.path.join(module_dir, "shedulers.py"), 'w') as file:
    file.write("import schedule\n")


with open(os.path.join(BASE_DIR, 'bot', 'schedulers.py'), 'a') as file:
    file.write("import {}.schedulers\n".format(module_name))

with open(os.path.join(BASE_DIR, 'bot', 'handlers.py'), 'a') as file:
    file.write("import {}.handlers\n".format(module_name))


