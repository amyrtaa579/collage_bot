import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from handlers import (
    start, specialties, quiz, admission, about, ai_agent  # добавили ai_agent
)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

dp = Dispatcher(storage=MemoryStorage())

# Регистрируем все роутеры
dp.include_router(start.router)
dp.include_router(specialties.router)
dp.include_router(quiz.router)
dp.include_router(admission.router)
dp.include_router(about.router)
dp.include_router(ai_agent.router)  # добавили

async def main() -> None:
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())