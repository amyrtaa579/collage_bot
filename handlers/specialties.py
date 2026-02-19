from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api.client import APIClient
from api.models.specialty import Specialty
from utils.formatters import format_specialty
from utils.filters import is_branch_specialty
from keyboards.callback_data import SpecialtyCallback

router = Router(name=__name__)


@router.message(F.text == "📚 СПЕЦИАЛЬНОСТИ")
@router.message(Command("specialties"))
async def list_specialties(message: Message):
    """Показывает список всех специальностей"""
    async with APIClient() as client:
        specialties_data = await client.get_specialties(limit=50)

    if not specialties_data:
        await message.answer("Список специальностей пуст.")
        return

    # Фильтруем специальности головного колледжа
    main_specialties = [s for s in specialties_data if not is_branch_specialty(s)]

    if not main_specialties:
        await message.answer("Нет доступных специальностей в головном колледже.")
        return

    builder = InlineKeyboardBuilder()
    for spec in main_specialties:
        spec_obj = Specialty.model_validate(spec)
        builder.button(
            text=f"{spec_obj.code} – {spec_obj.name}",
            callback_data=SpecialtyCallback(specialty_id=spec_obj.id, action="view").pack()
        )
    builder.button(text="◀️ НАЗАД", callback_data="back_to_main")
    builder.adjust(1)

    await message.answer(
        "Выберите специальность для просмотра:",
        reply_markup=builder.as_markup()
    )


@router.callback_query(SpecialtyCallback.filter(F.action == "view"))
async def show_specialty(callback: CallbackQuery, callback_data: SpecialtyCallback):
    """Показывает детальную информацию о специальности"""
    async with APIClient() as client:
        spec_data = await client.get_specialty(callback_data.specialty_id)

    if not spec_data:
        await callback.answer("Специальность не найдена", show_alert=True)
        return

    specialty = Specialty.model_validate(spec_data)
    text = format_specialty(specialty)
    
    # Добавляем кнопку НАЗАД
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ НАЗАД", callback_data="back_to_specialties")
    
    await callback.message.edit_text(
        text, 
        parse_mode="HTML",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "back_to_specialties")
async def back_to_specialties(callback: CallbackQuery):
    """Возврат к списку специальностей"""
    await callback.message.delete()
    await list_specialties(callback.message)
    await callback.answer()