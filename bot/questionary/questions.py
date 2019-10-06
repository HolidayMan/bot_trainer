from random import choice
from core.db import set_state, get_current_state
from bot.states.questionary_states import QuestionaryStates


QUESTION_1 = 'Как вас зовут?'
QUESTION_2 = 'Какая ваша фамилия?'
QUESTION_3 = 'Сколько вам лет?'
QUESTION_4 = 'Когда вам удобно планировать? (HH:MM:SS)'
QUESTION_5 = 'Вопрос 5'
QUESTION_6 = 'Вопрос 6'
QUESTION_7 = 'Вопрос 7'
QUESTION_8 = 'Вопрос 8'


class Questionary:
    _question_1 = ['Как вас зовут?']
    _question_2 = ['Какая ваша фамилия?']
    _question_3 = ['Сколько вам лет?']
    _question_4 = ['Когда вам удобно планировать? (HH:MM:SS)']
    _question_5 = ['Вопрос 5']
    _question_6 = ['Вопрос 6']
    _question_7 = ['Вопрос 7']
    _question_8 = ['Вопрос 8']

    
    @property
    def question_1(self):
        return self._question_1


    @question_1.getter
    def question_1(self):
        return choice(self._question_1)


    @property
    def question_2(self):
        return self._question_2


    @question_2.getter
    def question_2(self):
        return choice(self._question_2)


    @property
    def question_3(self):
        return self._question_3


    @question_3.getter
    def question_3(self):
        return choice(self._question_3)


    @property
    def question_4(self):
        return self._question_4


    @question_4.getter
    def question_4(self):
        return choice(self._question_4)


    @property
    def question_5(self):
        return self._question_5


    @question_5.getter
    def question_5(self):
        return choice(self._question_5)


    @property
    def question_6(self):
        return self._question_6


    @question_6.getter
    def question_6(self):
        return choice(self._question_6)


    @property
    def question_7(self):
        return self._question_7


    @question_7.getter
    def question_7(self):
        return choice(self._question_7)


    @property
    def question_8(self):
        return self._question_8


    @question_8.getter
    def question_8(self):
        return choice(self._question_8)


    def ask_question(self, bot_instance, message, question, state):
        chat_id = message.chat.id
        bot_instance.send_message(chat_id=chat_id, text=question)
        set_state(chat_id, state)
