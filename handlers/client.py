from create_bot import bot
from aiogram import Dispatcher, types

#@dp.message_handler()
async def start(message : types.Message):
    await bot.send_message(message.from_user.id, 'Привет')

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])