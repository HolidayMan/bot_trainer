from sqlalchemy import create_engine

DB_ENGINE = create_engine("sqlite:///sqlite.db") # change for connect your DB

STATES_FILE = 'states.vdb'

TOKEN = "123456789:your_token"

DEFAULT_HABBITS = ["planning"]


HABBITS = [
    'bot.plans',
    'bot.habbits', 
    'bot.questionary',
]
