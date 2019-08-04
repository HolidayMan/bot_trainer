from sqlalchemy.orm import sessionmaker
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
        if not self.user: # user isn't in db
            self.user = self.create(tguserobj)
            self.chat = self.create_chat(tguserobj, self.user)
        else:
            self.chat = self.get_chat(user=self.user)
        if self.user.first_name != tguserobj.first_name or self.user.username != tguserobj.username:
            self.update(tguserobj)
            
    
    def create(self, tguserobj):
        new_user = User(tg_id=tguserobj.id, first_name=tguserobj.first_name, username=tguserobj.username)
        self.session.add(new_user)
        self.session.commit()
        return new_user


    def create_chat(self, tgchatobj, user):
        chat = Chat(tg_id=tgchatobj.id, user=user)
        self.session.add(chat)
        self.session.commit()
        return chat


    def update(self, tguserobj):
        self.user.first_name = tguserobj.first_name
        self.user.username = tguserobj.username
        self.session.commit()


    def delete(self):
        self.session.delete(self.user)
        self.session.commit()
        del self


    def get_chat(tgchatobj=None, user=None):
        if tgchatobj:
            chat = self.session.query(Chat).filter(Chat.tg_id == tgchatobj.id).first()
        elif user:
            chat = self.session.query(Chat).join(Chat.user).filter(User.username == user.username).first()
        else:
            return None
        return chat

    
    @staticmethod
    def get_all_users():
        session = Session()
        users = session.query(User).all()
        session.close()
        return users


    def __del__(self):
        self.session.close()

