from sqlalchemy.orm import sessionmaker
from models.plan_model import Plan
from models.user_model import User
from bot.states.base_states import States
from vedis import Vedis

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
        session = Session()
        users = session.query(User).all()
        session.close()
        return users


class PlanDB(ObjectDB):
    def __init__(self, user_db_object=None, instance=None):
        if user_db_object:
            self.user = user_db_object.user
        elif instance:
            self.plan = instance


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
