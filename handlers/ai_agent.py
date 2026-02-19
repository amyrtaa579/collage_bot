from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router(name=__name__)


@router.message(F.text == "🤖 AI-АГЕНТ")
@router.message(Command("ai_agent"))
async def show_ai_agent(message: Message):
    """Показывает информацию об AI-агенте"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🤖 Перейти к AI-агенту", url="https://t.me/ai_tpgk_bot")
    builder.button(text="◀️ НАЗАД", callback_data="back_to_main")
    builder.adjust(1)
    
    await message.answer(
        "🤖 <b>AI-АГЕНТ ТПГК</b>\n\n"
        "Это умный помощник, который может:\n"
        "• Отвечать на вопросы о колледже\n"
        "• Помогать с выбором специальности\n"
        "• Рассказывать о правилах поступления\n"
        "• Консультировать по документам\n"
        "• И многое другое!\n\n"
        "Нажмите кнопку ниже, чтобы начать общение:",
        reply_markup=builder.as_markup()
    )


@router.callback_query(lambda c: c.data == "menu_ai_agent")
async def show_ai_agent_callback(callback: CallbackQuery):
    """Обработчик для вызова из главного меню"""
    await callback.message.delete()
    await show_ai_agent(callback.message)
    await callback.answer()