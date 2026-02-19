from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api.client import APIClient
from api.models.info_section import InfoSection
from utils.formatters import format_info_section

router = Router(name=__name__)

# Соответствие между callback и slug в API
ADMISSION_SLUGS = {
    "rules": "admission-rules",
    "privileges": "privileges",
    "loan": "educational-loan",
    "tuition": "tuition-fees",
    "docs": "documents",
    "methods": "application-methods",
}

ADMISSION_SECTIONS = {
    "rules": "📋 ПРАВИЛА ПРИЁМА",
    "privileges": "🎯 ЛЬГОТЫ",
    "loan": "💰 КРЕДИТОВАНИЕ",
    "tuition": "💵 СТОИМОСТЬ",
    "docs": "📄 ДОКУМЕНТЫ",
    "methods": "📨 СПОСОБЫ ПОДАЧИ",
}

@router.message(F.text == "📋 ПРИЁМНАЯ КОМИССИЯ")
@router.message(Command("admission"))
async def show_admission_menu(message: Message):
    """Показывает меню приёмной комиссии"""
    builder = InlineKeyboardBuilder()
    
    for callback, title in ADMISSION_SECTIONS.items():
        builder.button(text=title, callback_data=f"admission_{callback}")
    
    builder.button(text="◀️ НАЗАД", callback_data="back_to_main")
    builder.adjust(1)
    
    await message.answer(
        "📋 ПРИЁМНАЯ КОМИССИЯ",
        reply_markup=builder.as_markup()
    )


@router.callback_query(lambda c: c.data and c.data.startswith("admission_"))
async def show_admission_section(callback: CallbackQuery):
    """Загружает и показывает выбранный раздел из API"""
    section = callback.data.replace("admission_", "")
    slug = ADMISSION_SLUGS.get(section)
    
    if not slug:
        await callback.message.edit_text("Раздел не найден")
        await callback.answer()
        return
    
    await callback.answer("Загружаем информацию...")
    
    try:
        async with APIClient() as client:
            section_data = await client.get_info_section(slug)
        
        if not section_data:
            await callback.message.edit_text(
                f"{ADMISSION_SECTIONS[section]}\n\nИнформация временно недоступна",
                reply_markup=InlineKeyboardBuilder().button(
                    text="◀️ НАЗАД", 
                    callback_data="back_to_admission"
                ).as_markup()
            )
            await callback.answer()
            return
        
        section_obj = InfoSection.model_validate(section_data)
        text = format_info_section(section_obj)
        
        builder = InlineKeyboardBuilder()
        builder.button(text="◀️ НАЗАД", callback_data="back_to_admission")
        
        await callback.message.edit_text(
            text,
            reply_markup=builder.as_markup()
        )
        
    except Exception as e:
        await callback.message.edit_text(
            f"{ADMISSION_SECTIONS[section]}\n\nОшибка загрузки данных",
            reply_markup=InlineKeyboardBuilder().button(
                text="◀️ НАЗАД", 
                callback_data="back_to_admission"
            ).as_markup()
        )
    
    await callback.answer()


@router.callback_query(lambda c: c.data == "back_to_admission")
async def back_to_admission(callback: CallbackQuery):
    """Возврат в меню приёмной комиссии"""
    await callback.message.delete()
    await show_admission_menu(callback.message)
    await callback.answer()