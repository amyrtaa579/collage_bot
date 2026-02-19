from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router(name=__name__)


@router.message(F.text == "ℹ️ О колледже")
@router.message(Command("about"))
async def show_about_menu(message: Message):
    text = """
🏛 <b>ТОМСКИЙ ПРОМЫШЛЕННО-ГУМАНИТАРНЫЙ КОЛЛЕДЖ</b>

📅 <b>1987</b> - основан как ПТУ для Томского нефтехимкомбината
📅 <b>1990</b> - получил статус колледжа
📅 <b>2002</b> - преобразован в ТПГК

🏭 <b>СЕГОДНЯ</b>
• Современные лаборатории и полигоны
• Партнёры: Транснефть, СИБУР
• Центр прикладных квалификаций
• Стажировочная площадка для педагогов

🎓 <b>ВЫПУСКНИКИ</b>
• Более 7000 специалистов за 35 лет
• 30+ красных дипломов ежегодно
• Работа на ведущих предприятиях

✨ <b>МИССИЯ</b>
Качественное образование и развитие каждого студента

<i>«Учеба в ТПГК – путевка в успешную жизнь!»</i>
"""
    
    builder = InlineKeyboardBuilder()
    builder.button(text="📚 СПЕЦИАЛЬНОСТИ", callback_data="menu_specialties")
    builder.button(text="📋 ПРИЁМНАЯ КОМИССИЯ", callback_data="menu_admission")
    builder.button(text="◀️ НАЗАД", callback_data="back_to_main")
    builder.adjust(1)
    
    await message.answer(text, reply_markup=builder.as_markup())


@router.callback_query(lambda c: c.data == "menu_about")
async def show_about_callback(callback: CallbackQuery):
    await callback.message.delete()
    await show_about_menu(callback.message)
    await callback.answer()