from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from keyboards.reply import main_menu_keyboard

router = Router(name=__name__)

# Словарь со всеми разделами бота
MAIN_SECTIONS = {
    "admission": "📋 ПРИЁМНАЯ КОМИССИЯ",
    "specialties": "📚 СПЕЦИАЛЬНОСТИ",
    "quiz": "🎓 ПРОФОРИЕНТАЦИЯ",
    "about": "ℹ️ О КОЛЛЕДЖЕ",
    "ai_agent": "🤖 AI-АГЕНТ",
}

@router.message(CommandStart())
@router.message(Command("menu"))
async def show_main_menu(message: Message):
    user_name = message.from_user.first_name
    
    builder = InlineKeyboardBuilder()
    
    for callback_data, text in MAIN_SECTIONS.items():
        builder.button(text=text, callback_data=f"menu_{callback_data}")
    
    builder.adjust(1)
    
    welcome_text = (
        f"👋 <b>Привет, {user_name}!</b>\n\n"
        f"🤖 Я - официальный бот <b>Томского промышленно-гуманитарного колледжа</b>.\n"
        f"Помогу абитуриентам с поступлением.\n\n"
        f"📌 <b>Что я могу:</b>\n"
        f"• 📋 Всё о <b>приёмной комиссии</b> (правила, льготы, документы)\n"
        f"• 📚 Подробно о <b>специальностях</b>\n"
        f"• 🎓 <b>Профориентационный тест</b> для выбора профессии\n"
        f"• ℹ️ Информация <b>о колледже</b>\n"
        f"• 🤝 <b>AI-агент</b> для ответов на вопросы\n\n"
        f"⬇️ <b>Выбирай раздел в меню</b>"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )
    
    await message.answer(
        "Меню:",
        reply_markup=builder.as_markup()
    )


@router.message(lambda message: message.text == "🏠 Главное меню")
async def show_main_menu_from_button(message: Message):
    """Обработчик нажатия на кнопку Главное меню"""
    builder = InlineKeyboardBuilder()
    
    for callback_data, text in MAIN_SECTIONS.items():
        builder.button(text=text, callback_data=f"menu_{callback_data}")
    
    builder.adjust(1)
    
    menu_text = (
        "🏠 <b>ГЛАВНОЕ МЕНЮ</b>\n\n"
        "Выбери нужный раздел:\n\n"
        "📋 <b>ПРИЁМНАЯ КОМИССИЯ</b> — правила, льготы, документы\n"
        "📚 <b>СПЕЦИАЛЬНОСТИ</b> — подробное описание всех направлений\n"
        "🎓 <b>ПРОФОРИЕНТАЦИЯ</b> — тест для выбора профессии\n"
        "ℹ️ <b>О КОЛЛЕДЖЕ</b> — история и факты\n"
        "🤖 <b>AI-АГЕНТ</b> — задай вопрос в любое время"
    )
    
    await message.answer(
        menu_text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


@router.callback_query(lambda c: c.data and c.data.startswith("menu_"))
async def handle_menu_selection(callback: CallbackQuery, state: FSMContext):
    section = callback.data.replace("menu_", "")
    
    await callback.message.delete()
    
    if section == "admission":
        from handlers.admission import show_admission_menu
        await show_admission_menu(callback.message)
        
    elif section == "specialties":
        from handlers.specialties import list_specialties
        await list_specialties(callback.message)
        
    elif section == "quiz":
        from handlers.quiz import start_quiz
        await start_quiz(callback.message, state)
        
    elif section == "about":
        from handlers.about import show_about_menu
        await show_about_menu(callback.message)
        
    elif section == "ai_agent":
        builder = InlineKeyboardBuilder()
        builder.button(text="🤖 Перейти к AI-агенту", url="https://t.me/ai_tpgk_bot")
        builder.button(text="◀️ НАЗАД", callback_data="back_to_main")
        builder.adjust(1)
        
        await callback.message.answer(
            "🤖 <b>AI-АГЕНТ ТПГК</b>\n\n"
            "Задай ему любые вопросы о поступлении:\n"
            "• Документы и сроки\n"
            "• Специальности и баллы\n"
            "• Льготы и общежитие\n"
            "• И многое другое\n\n"
            "👇 Нажми кнопку и напиши ему!",
            reply_markup=builder.as_markup()
        )
    
    await callback.answer()


@router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.delete()
    await show_main_menu_from_button(callback.message)
    await callback.answer()