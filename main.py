import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
    
from config import BOT_TOKEN
from db import init_db
from handlers.client import router as client_router
from handlers.owner import router as owner_router


dp = Dispatcher()
dp.include_router(client_router)
dp.include_router(owner_router)

async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())