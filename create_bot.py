from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from brawlstats import Client


storage = MemoryStorage()

#bs = Client(os.getenv('API_TOKEN'))
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=storage)