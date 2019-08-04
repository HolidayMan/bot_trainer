from sqlalchemy.orm import sessionmaker
import os, sys
sys.path.append(os.getcwd())
from models.chat_model import Chat
from models.plan_model import Plan
from models.user_model import User

try:
    from local_settings.config import DB_ENGINE
except ImportError:
    from prod_settings.config import DB_ENGINE

engine = DB_ENGINE
Session = sessionmaker(bind=engine)

class UserDB:
    
    def __init__(self, tguserobj):
        self.session = Session()
        self.user = self.session.query(User).filter(User.tg_id == tguserobj.id).first()
        if self.user.first_name != tguserobj.first_name or self.user.username != tguserobj.username:
            self.update(tguserobj)
        if not self.user: # user isn't in db
            self.user = self.create(tguserobj)
            
    
    def create(self, tguserobj):
        new_user = User(tg_id=tguserobj.id, first_name=tguserobj.first_name, username=tguserobj.username)
        self.session.add(new_user)
        self.session.commit()
        return new_user


    def update(self, tguserobj):
        self.user.first_name = tguserobj.first_name
        self.user.username = tguserobj.username
        self.session.commit()


    def delete(self):
        self.session.delete(self.user)
        self.session.commit()
        del self


    @staticmethod
    def create_user(tguserobj):
        session = Session()
        user = User(tg_id=tguserobj.id, first_name=tguserobj.first_name, username=tguserobj.username)
        session.add(user)
        session.commit()
        session.close()
        return user


    @staticmethod
    def get_user(tguserobj):
        session = Session()
        user = session.query(User).filter(User.tg_id == tguserobj.id).first()
        session.close()
        return user


    @staticmethod
    def update_user(tguserobj):
        session = Session()
        user = session.query(User).filter(User.tg_id == tguserobj.id).first()
        user.first_name = tguserobj.first_name
        user.username = tguserobj.username
        session.commit()
        session.close()
        return user
    

    @staticmethod
    def delete_user(tguserobj):
        session = Session()
        user = session.query(User).filter(User.tg_id == tguserobj.id).first()
        session.delete(user)
        session.commit()
        session.close()


    def __del__(self):
        self.session.close()
