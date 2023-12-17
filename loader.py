from aiogram import Bot, Dispatcher
from configparser import ConfigParser
from aiogram.contrib.fsm_storage.memory import MemoryStorage

config = ConfigParser()
config.read('config.ini')
token = config.get("mainConf", "token")

storage = MemoryStorage()

bot = Bot(token, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)