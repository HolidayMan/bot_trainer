from sqlalchemy import create_engine
from models.plan_model import Plan
from models.user_model import User
from models.habbit_model import Habbit
from models.base import Base, habbits2create
from sqlalchemy.orm import sessionmaker

try:
    from local_settings.config import DB_ENGINE
except ImportError:
    from prod_settings.config import DB_ENGINE

engine = DB_ENGINE
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

for habbit in habbits2create:
    session.add(Habbit(en_name=habbit.Meta.en_name, ru_name=habbit.Meta.ru_name))

session.commit()
session.close()
