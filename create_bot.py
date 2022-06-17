import sqlite3
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from brawlstats import Client


storage = MemoryStorage()

bs = Client(os.getenv('API_TOKEN'))
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=storage)
con = sqlite3.connect("brawl.db")
cursor = con.cursor()