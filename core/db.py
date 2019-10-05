from sqlalchemy.orm import sessionmaker

from models.plan_model import Plan
from models.user_model import User
from models.habbit_model import Habbit

from bot.states.base_states import States
from vedis import Vedis

from .exceptions import *

try:
    import local_settings.config as config
except ModuleNotFoundError:
    import prod_settings.config as config

engine = config.DB_ENGINE
Session = sessionmaker(bind=engine)


class ObjectDB:
    session = Session()


    def __del__(self):
        self.session.close()


class UserDB(ObjectDB):
    
    def __init__(self, tguserobj):
        self.user = self.session.query(User).filter(User.tg_id == tguserobj.id).first()
        if not self.user: # user isn't in db
            self.user = self.create(tguserobj)
        if self.user.first_name != tguserobj.first_name or self.user.username != tguserobj.username:
            self.update(tguserobj)
            
    
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
    def get_all_users():
        try:
            session = Session()
            users = session.query(User).all()
            session.close()
        except:
            session = ObjectDB.session
            users = session.query(User).all()
        return users


class PlanDB(ObjectDB):
    def __init__(self, user_db_object=None, instance=None):
        if user_db_object:
            self.user = user_db_object.user
        if instance:
            self.plan = self.session.query(Plan).filter(Plan.id == instance.id).first()


    def create(self, title=None, type=None, user=None, plan=None):
        if not plan:
            new_plan = Plan(title=title, type=type, status=Plan.STATUS_WAIT, user=self.user if not user else user)
        else:
            new_plan = plan
        self.session.add(new_plan)
        self.session.commit()
        return new_plan

    
    def get_all_plans(self, status=None, type=None):
        plans_query = self.session.query(Plan).join(Plan.user).filter(User.id == self.user.id)
        if status:
            plans_query = plans_query.filter(Plan.status == status)
        if type:
            plans_query = plans_query.filter(Plan.type == type)
        return plans_query.order_by(Plan.status).all()
    

    def mark_canceled(self):
        if not self.plan:
            return
        self.plan.status = Plan.STATUS_CANCELED
        self.session.commit()

    
    def mark_done(self):
        if not self.plan:
            print("\n\n\nHello\n\n\n")
            return
        self.plan.status = Plan.STATUS_DONE
        self.session.commit()
    

    def mark_overdue(self):
        if not self.plan:
            return
        if self.plan.is_overdue() and self.plan.status != Plan.STATUS_OVERDUE:
            self.plan.status = Plan.STATUS_OVERDUE
            self.session.commit()


    def mark_wait(self):
        if not self.plan:
            return
        self.plan.status = Plan.STATUS_WAIT
        self.session.commit()


    def delete(self):
        if not self.plan:
            return
        self.session.delete(self.plan)
        self.session.commit()


def set_state(user_id, value):
    with Vedis(config.STATES_FILE) as db:
        try:
            db[user_id] = value
            return True
        except:
            return False


def get_current_state(user_id):
    with Vedis(config.STATES_FILE) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return States.S_ENTERCOMMAND.value


class HabbitDB(ObjectDB):
    def __init__(self, user_db_object=None, instance=None, en_name=None, ru_name=None):
        if user_db_object:
            self.user = user_db_object.user
        if instance:
            self.set_habbit(instance.en_name, instance.ru_name)
        if en_name or ru_name:
            self.set_habbit(en_name, ru_name)

    
    def set_habbit(self, en_name=None, ru_name=None):
        if en_name:
            self.habbit = self.session.query(Habbit).filter(Habbit.en_name == en_name).first()
        elif ru_name:
            self.habbit = self.session.query(Habbit).filter(Habbit.ru_name == ru_name).first()
        return self.habbit


    def get_all_users(self):
        if not self.habbit:
            return
        return self.habbit.users


    def get_all_habbits(self):
        habbits = self.session.query(Habbit).all()
        if self.user:
            user_habbits = self.user.habbits
        else:
            user_habbits = []
        return list(set(habbits) ^ set(user_habbits))


    def set_user_habbit(self): # sets a new habbit for user
        if not self.user or not self.habbit:
            return 
        
        if not self.habbit in self.user.habbits:
            if len(self.user.habbits) < 3:
                self.user.habbits.append(self.habbit)
                self.session.commit()
            else:
                raise ValueError("Max amount of habbits is 3")
        else:
            raise ValueError("User already has this habbit")
        
    
    def unset_user_habbit(self): # unsets a gabbit for user
        if not self.user or not self.habbit:
            return 
        
        self.user.habbits.pop(self.user.habbits.index(self.habbit))
        self.session.commit()


class UserInfoDB(ObjectDB):
    user_info = None

    def __init__(self, user_info_obj=None):
        if user_info_obj:
            self.user_info = user_info_obj
    
    
    def save(self):
        if not self.user_info:
            raise NoUserInfoToSave("user_info attribute was not defined")
        
        self.session.add(self.user_info)
        self.session.commit()
