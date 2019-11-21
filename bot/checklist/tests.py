import unittest
import time
import json

from telebot import types

from core.db import get_current_state, set_cmd_state
from bot.bot import bot
from bot.buffer import Buffer
from models.project_model import Project
from bot.states.checklist_states import ChecklistStates

from .handlers import cmd_add_project, project_name_handler, project_date_handler
from .microlessons import get_lt_from_number
import bot.checklist.phrases as ph
message_json = '{"message_id":611,"from":{"id":384612009,"is_bot":false,"first_name":"let45fc","username":"let45fc","language_code":"ru"},"chat":{"id":384612009,"first_name":"let45fc","username":"let45fc","type":"private"},"date":1572038731,"text":"Hello"}'

class TestQuestionaryHanlers(unittest.TestCase):

    def send_message(self, fun, text, *args, **kwargs):
        self.message.text = text
        answer = fun(self.message, *args, **kwargs)
        if type(answer) != tuple:
            self.answers.append(answer)
        else:
            self.answers.extend(answer)
        return answer

    def delete_message(self, message):
        if not message:
            return
        while True:
            try:
                bot.delete_message(message.chat.id, message.message_id)
                break
            except:
                time.sleep(0.1)

    @classmethod
    def setUpClass(cls):
        cls.buffer = Buffer()
        cls.message = types.Message.de_json(json.loads(message_json))
        cls.answers = []
    
    
    def test_add_project_handler(self):
        self.message.text = "/add_project"
        answer = cmd_add_project(self.message)
        self.answers.append(answer)
        self.assertEqual(get_current_state(384612009), ChecklistStates.STATE_MCL_1.value)
        self.assertEqual(answer.text, get_lt_from_number(1).strip())


    def test_project_name_handler(self):
        self.message.text = "Тестовый проект"
        answer = project_name_handler(self.message)
        self.answers.append(answer)
        self.assertEqual(get_current_state(384612009), ChecklistStates.STATE_MCL_2.value)
        self.assertEqual(answer.text, get_lt_from_number(2).strip())
        self.buffer.update()
        buffer_key = str(self.message.chat.id) + 'new_project'
        self.assertEqual(self.buffer[buffer_key], Project(name=self.message.text))


    def test_project_date_handler(self):
        answer = self.send_message(project_date_handler, "Shit")
        self.assertEqual(answer[0].text, ph.INCORRECT_DATE)

        answer = self.send_message(project_date_handler, "21.11.19-30.11.19")
        self.assertEqual(get_current_state(384612009), ChecklistStates.STATE_MCL_3.value)
        self.assertEqual(answer[0].text, ph.PROJECT_ADDED)
        self.assertEqual(answer[1].text, get_lt_from_number(3).strip())


    def tearDown(self):
        for answer in self.answers:
            self.delete_message(answer)
        self.answers.clear()

    
    @classmethod
    def tearDownClass(cls):
        set_cmd_state(cls.message.chat.id)
        cls.buffer.clean_for_user(cls.message.chat.id)
        cls.buffer.save()


if __name__ == "__main__":
    unittest.main()