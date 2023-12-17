from loader import bot, dp
from aiogram.utils import executor
import asyncio
from database import db

from handlers import register

register.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)