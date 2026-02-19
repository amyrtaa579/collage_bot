import asyncio
from typing import Optional
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.reply import main_menu_keyboard
from states.quiz import QuizState
from utils.quiz_data import (
    QUESTIONS, get_initial_scores, get_top_specialties,
    filter_scores_by_gender, MOTIVATION_TEXTS, SPECIALTIES
)
from api.client import APIClient
from api.models.specialty import Specialty
from utils.formatters import format_specialty
from keyboards.callback_data import SpecialtyCallback

router = Router(name=__name__)


@router.message(F.text == "🎓 Профориентация")
@router.message(Command("quiz"))
async def start_quiz(message: Message, state: FSMContext):
    """Начинаем тест с вопроса о поле"""
    await state.set_data({"scores": get_initial_scores(), "current_q": 0})
    await state.set_state(QuizState.gender)
    
    builder = InlineKeyboardBuilder()
    builder.button(text="👨 Парень", callback_data="gender_male")
    builder.button(text="👩 Девушка", callback_data="gender_female")
    builder.adjust(1)
    
    await message.answer(
        "Для точного подбора профессии укажи свой пол:",
        reply_markup=builder.as_markup()
    )


@router.callback_query(lambda c: c.data.startswith("gender_"))
async def process_gender(callback: CallbackQuery, state: FSMContext):
    """Сохраняем пол и переходим к первому вопросу"""
    await callback.answer()
    gender = callback.data.split("_")[1]
    
    await state.update_data(gender=gender)
    await state.set_state(QuizState.q1)
    await callback.message.delete()
    await ask_question(callback.message, state, 0)


async def ask_question(message: Message, state: FSMContext, q_index: int):
    """Отправляет вопрос с вариантами ответов"""
    question_text, options = QUESTIONS[q_index]
    
    builder = InlineKeyboardBuilder()
    for i, (opt_text, _) in enumerate(options):
        builder.button(
            text=opt_text,
            callback_data=f"quiz_answer:{q_index}:{i}"
        )
    builder.button(text="Завершить", callback_data="quiz_exit")
    builder.adjust(1)

    await message.answer(
        f"Вопрос {q_index+1} из {len(QUESTIONS)}\n\n{question_text}",
        reply_markup=builder.as_markup()
    )


@router.callback_query(lambda c: c.data.startswith("quiz_answer:"))
async def handle_quiz_answer(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает ответ на вопрос"""
    await callback.answer()
    
    _, q_index_str, answer_index_str = callback.data.split(":")
    q_index = int(q_index_str)
    answer_index = int(answer_index_str)
    
    _, options = QUESTIONS[q_index]
    _, weights = options[answer_index]
    
    data = await state.get_data()
    scores = data.get("scores", get_initial_scores())
    current_q = data.get("current_q", 0)
    
    for code, points in weights.items():
        scores[code] = scores.get(code, 0) + points
    
    next_q = current_q + 1
    if next_q >= len(QUESTIONS):
        await state.update_data(scores=scores)
        user_name = callback.from_user.first_name or "Абитуриент"
        await callback.message.delete()
        await finish_quiz(callback.message, state, user_name)
        return
    
    await state.update_data(scores=scores, current_q=next_q)
    states = [
        QuizState.q1, QuizState.q2, QuizState.q3, QuizState.q4,
        QuizState.q5, QuizState.q6, QuizState.q7, QuizState.q8
    ]
    await state.set_state(states[next_q])
    
    await callback.message.delete()
    await ask_question(callback.message, state, next_q)


@router.callback_query(lambda c: c.data == "quiz_exit")
async def quiz_exit(callback: CallbackQuery, state: FSMContext):
    """Досрочный выход из теста"""
    await callback.answer()
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "Тест прерван.",
        reply_markup=main_menu_keyboard()
    )


async def get_specialty_by_code_from_list(client: APIClient, code: str) -> Optional[Specialty]:
    """Получает специальность по коду из списка"""
    specialties_data = await client.get_specialties(limit=100)
    if not specialties_data:
        return None
    
    for spec_data in specialties_data:
        if spec_data.get("code") == code:
            return Specialty.model_validate(spec_data)
    return None


async def finish_quiz(message: Message, state: FSMContext, user_name: str):
    """Показывает результаты теста"""
    data = await state.get_data()
    scores = data["scores"]
    gender = data.get("gender", "male")
    
    filtered_scores = filter_scores_by_gender(scores, gender)
    top_specs = get_top_specialties(filtered_scores)

    specs_full = []
    async with APIClient() as client:
        for code, name, points in top_specs:
            specialty = await get_specialty_by_code_from_list(client, code)
            if specialty:
                specs_full.append((specialty, points))
            else:
                dummy = Specialty(
                    code=code, 
                    name=name,
                    description=f"Информация о специальности {name}",
                    id=None
                )
                specs_full.append((dummy, points))

    text = f"🌟 {user_name}, твои результаты:\n\n"
    text += "🎯 Лучшие варианты:\n\n"

    for idx, (specialty, points) in enumerate(specs_full, 1):
        medal = "🥇" if idx == 1 else "🥈"
        text += f"{medal} {specialty.name}\n"
        mot = MOTIVATION_TEXTS.get(specialty.code, "Эта профессия тебе подходит!")
        text += f"   {mot}\n\n"

    builder = InlineKeyboardBuilder()
    for specialty, _ in specs_full:
        if specialty.id:
            builder.button(
                text=f"🔍 {specialty.name}",
                callback_data=SpecialtyCallback(specialty_id=specialty.id, action="view").pack()
            )
    
    builder.button(text="🏠 Главное меню", callback_data="back_to_main")
    builder.adjust(1)

    await message.answer(
        text,
        reply_markup=builder.as_markup()
    )
    await state.clear()