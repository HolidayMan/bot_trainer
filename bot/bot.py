import telebot
import sys
try:
    import local_settings.config as config
except ModuleNotFoundError:
    import prod_settings.config as config

bot = telebot.TeleBot(config.TOKEN)