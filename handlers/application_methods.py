from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api.client import APIClient
from api.models.application_method import ApplicationMethod

router = Router(name=__name__)


@router.message(F.text == "📨 Способы подачи документов")
@router.message(Command("application_methods"))
async def show_application_methods(message: Message):
    """Показывает способы подачи документов"""
    async with APIClient() as client:
        methods_data = await client.get_application_methods()
    
    if not methods_data:
        await message.answer(
            "Информация о способах подачи документов временно недоступна.",
            reply_markup=InlineKeyboardBuilder().button(
                text="◀️ Назад", 
                callback_data="back_to_main"
            ).as_markup()
        )
        return
    
    # Форматируем вывод
    text = "📨 <b>Способы подачи документов</b>\n\n"
    
    for method_data in methods_data:
        method = ApplicationMethod.model_validate(method_data)
        text += f"<b>• {method.name}</b>\n"
        text += f"{method.description}\n"
        if method.icon:
            text += f"  {method.icon}\n"
        text += "\n"
    
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ Назад в меню", callback_data="back_to_main")
    
    await message.answer(text, reply_markup=builder.as_markup())


# Добавим обработчик для inline-кнопки из главного меню
@router.callback_query(lambda c: c.data == "menu_application_methods")
async def show_application_methods_callback(callback: CallbackQuery):
    """Обработчик для вызова из главного меню"""
    await callback.message.delete()
    await show_application_methods(callback.message)
    await callback.answer()