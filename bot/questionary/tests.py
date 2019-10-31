import unittest
from .handlers import *
from telebot import types
import json
import time
from datetime import time as new_time

from bot.buffer import Buffer
from core.db import set_cmd_state
from bot.bot import bot

from .phrases import *
from .questions import *


message_json = '{"message_id":611,"from":{"id":384612009,"is_bot":false,"first_name":"let45fc","username":"let45fc","language_code":"ru"},"chat":{"id":384612009,"first_name":"let45fc","username":"let45fc","type":"private"},"date":1572038731,"text":"Hello"}'

class TestQuestionaryHanlers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.buffer = Buffer()
        cls.message = types.Message.de_json(json.loads(message_json))
        cls.answers = []
        cls.questionary = Questionary()
    
    
    def test_handler_1_english(self):
        self.message.text = "Hello"
        answer = handle_answer_1(self.message)
        self.answers.extend(answer)
        # [self.answers.append(i) for i in answer]
        self.assertEqual(answer[0].text, GREAT)
        self.assertEqual(answer[1].text, self.questionary.question_2)
        

    def test_handler_1_russian(self):
        self.message.text = "Приветулио"
        answer = handle_answer_1(self.message)
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, GREAT)
        self.assertEqual(answer[1].text, self.questionary.question_2)


    def test_handler_1_not_text(self):
        self.message.text = "111"
        answer = handle_answer_1(self.message)
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, PHRASE_NAME_MUST_CONTAIN_JUST_LETTERS)

        self.message.text = None
        answer = handle_answer_1(self.message)
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, PHRASE_NAME_MUST_CONTAIN_JUST_LETTERS)
        

    def test_handler_2_english(self):
        self.message.text = "Hello"
        answer = handle_answer_2(self.message)
        self.answers.extend(answer)
        # [self.answers.append(i) for i in answer]
        self.assertEqual(answer[0].text, GREAT)
        self.assertEqual(answer[1].text, self.questionary.question_3)
        

    def test_handler_2_russian(self):
        self.message.text = "Приветулио"
        answer = handle_answer_2(self.message)
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, GREAT)
        self.assertEqual(answer[1].text, self.questionary.question_3)


    def test_handler_2_not_text(self):
        self.message.text = "111"
        answer = handle_answer_2(self.message)
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, PHRASE_SURNAME_MUST_CONTAIN_JUST_LETTERS)

        self.message.text = None
        answer = handle_answer_2(self.message)
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, PHRASE_SURNAME_MUST_CONTAIN_JUST_LETTERS)


    def test_handler_3(self):
        self.message.text = "15"
        answer = handle_answer_3(self.message)
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, GREAT)
        self.assertEqual(answer[1].text, self.questionary.question_4)

        self.message.text = "130"
        answer = handle_answer_3(self.message)
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, AGE_MUST_BE_A_NUMBER_AND_BETWEEN)

        self.message.text = "-1000"
        answer = handle_answer_3(self.message)
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, AGE_MUST_BE_A_NUMBER_AND_BETWEEN)


    def test_handler_4(self):
        self.message.text = "23:24:24"
        answer = handle_answer_4(self.message)
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, GREAT)
        self.assertEqual(answer[1].text, self.questionary.question_5)
        chat_id = self.message.chat.id
        buffer_key = str(chat_id)+"questionary"
        self.buffer.update()
        userinfo = self.buffer.get(buffer_key)
        self.assertEqual(userinfo.planning_time, new_time(23, 24, 24))

        self.message.text = "hello"
        answer = handle_answer_4(self.message) 
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, TIME_MUST_BE_FORMAT)

        self.message.text = "25:00:00"
        answer = handle_answer_4(self.message)
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, INVALID_TIME_FORMAT)


    def test_handler_5(self):
        self.message.text = "Answer 5"
        answer = handle_answer_5(self.message)
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, GREAT)
        self.assertEqual(answer[1].text, self.questionary.question_6)

        chat_id = self.message.chat.id
        buffer_key = str(chat_id)+"questionary"
        self.buffer.update()
        userinfo = self.buffer.get(buffer_key)
        self.assertEqual(userinfo.question1, "Answer 5")


    def test_handler_6(self):
        self.message.text = "Answer 6"
        answer = handle_answer_6(self.message)
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, GREAT)
        self.assertEqual(answer[1].text, self.questionary.question_7)

        chat_id = self.message.chat.id
        buffer_key = str(chat_id)+"questionary"
        self.buffer.update()
        userinfo = self.buffer.get(buffer_key)
        self.assertEqual(userinfo.question2, "Answer 6")


    def test_handler_7(self):
        self.message.text = "Answer 7"
        answer = handle_answer_7(self.message)
        self.answers.extend(answer)
        self.assertEqual(answer[0].text, GREAT)
        self.assertEqual(answer[1].text, self.questionary.question_8)

        chat_id = self.message.chat.id
        buffer_key = str(chat_id)+"questionary"
        self.buffer.update()
        userinfo = self.buffer.get(buffer_key)
        self.assertEqual(userinfo.question3, "Answer 7")


    def tearDown(self):
        time.sleep(0.3)
        for answer in self.answers:
            try:
                bot.delete_message(answer.chat.id, answer.message_id)
            except:
                pass


    @classmethod
    def tearDownClass(cls):
        set_cmd_state(cls.message.chat.id)
        cls.buffer.clean_for_user(cls.message.chat.id)
        cls.buffer.save()
        
        
if __name__ == "__main__":
	unittest.main()
