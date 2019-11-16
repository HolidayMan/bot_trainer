from sqlalchemy import create_engine
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DB_ENGINE = create_engine("sqlite:///sqlite.db") # change for connect your DB

STATES_FILE = 'states.vdb'

TOKEN = "123456789:your_token"

DEFAULT_HABBITS = ["planning"]

ARTICLES_PATH = os.path.join(BASE_DIR, 'articles')

HABBITS = [
    'plans',
    'habbits', 
    'questionary',
]
