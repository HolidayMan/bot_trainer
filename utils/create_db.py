import os, sys
sys.path.append(os.path.dirname(os.getcwd()))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.chat_model import Chat
from models.plan_model import Plan
from models.user_model import User
from models.base import Base

try:
    from local_settings.config import DB_ENGINE
except ImportError:
    from prod_settings.config import DB_ENGINE

engine = DB_ENGINE
Base.metadata.create_all(bind=engine)



