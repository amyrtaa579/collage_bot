from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="🎓 Профориентация")],
        [KeyboardButton(text="ℹ️ О колледже"), KeyboardButton(text="🏠 Главное меню")],
        
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)