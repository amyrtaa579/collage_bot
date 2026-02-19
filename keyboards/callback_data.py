from aiogram.filters.callback_data import CallbackData

class SpecialtyCallback(CallbackData, prefix="spec"):
    specialty_id: int
    action: str  # например, "view"