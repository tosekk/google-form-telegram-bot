"""This file creates and runs the bot.
"""

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from config import TOKEN


memory = MemoryStorage()
bot = Bot(TOKEN, parse_mode='html')
dp = Dispatcher(bot, storage=memory)


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(dp)