try:
    import local_settings.config as config
except ModuleNotFoundError:
    import prod_settings.config as config
import importlib
[importlib.import_module(f'bot.{habbit}.handlers', package='*') for habbit in config.HABBITS]
