import unittest
import importlib
import sys
if len(sys.argv) > 1:
    modules = sys.argv[1:]
    sys.argv = sys.argv[:1]

    imports = [importlib.import_module(f'bot.{module}.tests') for module in modules]
else:
    try:
        from local_settings.config import HABBITS
    except ModuleNotFoundError:
        from prod_settings.config import HABBITS

    imports = [importlib.import_module(f'bot.{habbit}.tests') for habbit in HABBITS]
[globals().update({name: class_}) for module in imports for name, class_ in vars(module).items() if name.startswith('Test')]

if __name__ == "__main__":
    unittest.main()
    