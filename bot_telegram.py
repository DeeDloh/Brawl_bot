from aiogram.utils import executor
from create_bot import dp

async def on_startup(_):
    print('Бот онлайн')

from handlers import client, others

client.register_handlers_client(dp)
others.register_handlers_others(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)