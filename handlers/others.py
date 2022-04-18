from create_bot import bot
from aiogram import Dispatcher, types

#@dp.message_handler()
async def echo_send(message : types.Message):
    await bot.send_message(message.from_user.id, message.text)

def register_handlers_others(dp : Dispatcher):
    dp.register_message_handler(echo_send)