from local_settings.config import HABBITS
import importlib
[importlib.import_module(f'bot.{habbit}.schedulers', package='*') for habbit in HABBITS]
