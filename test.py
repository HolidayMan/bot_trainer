import unittest
import importlib
try:
    from local_settings.config import HABBITS
except ModuleNotFoundError:
    from prod_settings.config import HABBITS

imports = [importlib.import_module(f'{habbit}.tests', package='*') for habbit in HABBITS]
# imports = eval(f'from bot.questionary.tests import *')
from bot.questionary.tests import *

f = open('tests.py', 'r')
unittest.main()
