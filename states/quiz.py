# states/quiz.py
from aiogram.fsm.state import State, StatesGroup

class QuizState(StatesGroup):
    gender = State()          # вопрос о поле
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()
    finish = State()