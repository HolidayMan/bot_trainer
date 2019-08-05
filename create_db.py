from sqlalchemy import create_engine
from models.plan_model import Plan
from models.user_model import User
from models.base import Base

try:
    from local_settings.config import DB_ENGINE
except ImportError:
    from prod_settings.config import DB_ENGINE

engine = DB_ENGINE
Base.metadata.create_all(bind=engine)
