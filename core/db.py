from sqlalchemy.orm import sessionmaker
from vedis import Vedis

from bot.states.base_states import States
from models.habbit_model import Habbit
from models.plan_model import Plan
from models.studying_model import Studying
from models.user_info_model import UserInfo
from models.user_model import User
from models.project_model import Project
from models.task_model import Task
from models.performer_model import Performer

import core.exceptions as exc

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
            raise exc.NoPlanDefinedError("self.plan was not defined")
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


def set_cmd_state(user_id):
    with Vedis(config.STATES_FILE) as db:
        try:
            db[user_id] = States.S_ENTERCOMMAND.value
            return True
        except:
            return False


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


class UserInfoDB(ObjectDB): # CRU
    user_info = None

    def __init__(self, userdb_obj=None, user_info_obj=None, user=None):
        if user_info_obj:
            self.user_info = user_info_obj
        if userdb_obj:
            self.user = userdb_obj.user
            self.user_info = self.get_user_info()
        if user:
            self.user = user
            self.user_info = self.get_user_info()
    
    
    def save(self):
        if not self.user_info:
            raise exc.NoUserInfoToSave("user_info attribute was not defined")
        
        self.session.add(self.user_info)
        self.session.commit()


    def get_user_info(self):
        if not self.user:
            raise exc.NoUserToGetInfo("user attribute was not defined")
    
        user_info = self.session.query(UserInfo).filter(UserInfo.user_id == self.user.id).first()
        return user_info


class StudyingDB(ObjectDB): # CRU
    studying = None

    def __init__(self, userdb_obj=None, user=None, studying_obj=None, state=None):
        if userdb_obj:
            self.user = userdb_obj.user
        if user:
            self.user = user
        if user and (state is not None):
            self.user = user
            query = self.session.query(Studying).filter(Studying.user_id == self.user.id)
            query_list = query.all()
            if query_list:
                self.studying = query_list[0]
                if self.studying.state != state:
                    self.studying.state = state
                    self.save()
            else:
                self.studying = Studying(user=self.user, state=state)
                self.save()
        elif studying_obj:
            self.studying = studying_obj
            self.user = studying_obj.user


    def save(self):
        if not self.studying:
            raise exc.NoStudyingToSave("studying attribute was not defined")
        
        self.session.add(self.studying)
        self.session.commit()


    def get_user_studying(self):
        if not self.user:
            raise exc.NoUserToGetInfo("user attribute was not defined")

        self.studying = self.session.query(Studying).filter(Studying.user_id == self.user.id).first()
        return self.studying


class ProjectDB(ObjectDB):
    project = None

    def __init__(self, user_db_object=None, instance=None):
        if user_db_object:
            self.user = user_db_object.user
        if instance:
            self.project = self.session.query(Project).filter(Project.id == instance.id).first()


    def create(self, name=None, date_start=None, date_end=None, user=None):
        if not self.project:
            new_project = Project(name=name, date_start=date_start, date_end=date_end, user=self.user if not user else user)
        else:
            new_project = self.project
        self.session.add(new_project)
        self.session.commit()
        return new_project

    
    def get_all_projects(self):
        projects_query = self.session.query(Project).join(Project.user).filter(User.id == self.user.id)
        return projects_query.order_by(Project.date_start).all()

    
    def mark_completed(self):
        if not self.project:
            raise exc.NoProjectDefinedError("self.project was not defined")
        self.project.completed = True
        self.session.commit()


    def mark_not_completed(self):
        if not self.project:
            raise exc.NoProjectDefinedError("self.project was not defined")
        self.project.completed = False
        self.session.commit()


    def delete(self):
        if not self.project:
            return
        self.session.delete(self.project)
        self.session.commit()


class TaskDB(ObjectDB):
    task = None

    def __init__(self, user_db_object=None, project=None, instance=None):
        if user_db_object:
            self.user = user_db_object.user
        if project:
            self.project = project
        if instance:
            self.task = self.session.query(Task).filter(Task.id == instance.id).first()


    def create(self, name=None, date_start=None, duration=None, permormers=None, comments=None, project=None):
        if not self.task:
            new_task = Project(name=name, date_start=date_start, duration=duration, project=project)
        else:
            new_task = self.task
        self.session.add(new_task)
        self.session.commit()
        return new_task

    
    def get_all_tasks(self):
        tasks_query = self.session.query(Task).join(Task.project).filter(Project.id == self.project.id)
        return tasks_query.order_by(Task.date_start).all()

    
    def mark_completed(self):
        if not self.task:
            raise exc.NoTaskDefinedError("self.task was not defined")
        self.task.completed = True
        self.session.commit()


    def mark_not_completed(self):
        if not self.task:
            raise exc.NoTaskDefinedError("self.task was not defined")
        self.task.completed = False
        self.session.commit()


    def get_performers(self):
        if not self.task:
            raise exc.NoTaskDefinedError("self.task was not defined")
        try:
            return self.task.performers
        except:
            self = TaskDB(instance=self.task)
            return self.task.performers


    def delete(self):
        if not self.task:
            return
        self.session.delete(self.task)
        self.session.commit()


class PerformerDB(ObjectDB):
    performer = None

    def __init__(self, user_db_object=None, task=None, instance=None):
        if user_db_object:
            self.user = user_db_object.user
        if task:
            self.task = task
        if instance:
            self.performer = self.session.query(Performer).filter(Performer.id == instance.id).first()


    def create(self, name=None, phone_number=None, comments=None, user=None):
        if not self.performer:
            new_performer = Performer(name=name, phone_number=phone_number, comments=comments, user=user)
        else:
            new_performer = self.performer
        self.session.add(new_performer)
        self.session.commit()
        return new_performer

    
    def get_all_tasks(self):
        performers_query = self.session.query(Performer).join(Performer.task).filter(Task.id == self.task.id)
        return performers_query.order_by(Performer.id).all()


    def delete(self):
        if not self.performer:
            return
        self.session.delete(self.performer)
        self.session.commit()
        