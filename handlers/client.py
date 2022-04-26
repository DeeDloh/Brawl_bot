from aiogram import Dispatcher, types
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types  import ReplyKeyboardRemove
from keyboards import kb_ts
import requests


def find_map(map_name):
    all_map = requests.get('https://api.brawlapi.com/v1/maps').json()
    for map in all_map['list']:
        if map_name == map['name']:
            return map['id']
    return None


class FSMMap(StatesGroup):
    map_id = State()
    team_solo_stats = State()


#@dp.message_handler(commands='Карты')
async def cm_start(message : types.Message):
    await FSMMap.map_id.set()
    await bot.send_message(message.chat.id, 'Введите название карты(на английском)')


#@dp.message_handler(state=FSMMap.map_id)
async def map_n(message : types.Message, state : FSMContext):
    if message.text.lower() == 'назад':
        await   bot.send_message(message.chat.id, 'Введите название карты(на английском)',
                               reply_markup=ReplyKeyboardRemove())
    async with state.proxy() as data:

        if find_map(message.text) is None:
            await bot.send_message(message.chat.id, 'Такой карты нет')

            await FSMMap.previous()
        else:
            data['map_id'] = find_map(message.text)
            await FSMMap.next()
            await bot.send_message(message.chat.id, 'Выбери на кого выдавать статистику', reply_markup=kb_ts)


#@dp.message_handler(state=FSMMap.team_solo_stats)
async def t_s_map(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        if message.text.lower() in ['тим', 'соло']:
            if message.text.lower() == 'тим':
                data['team_solo_stats'] = 'team'
            else:
                data['team_solo_stats'] = 'solo'
            await bot.send_message(message.chat.id, str(data), reply_markup=ReplyKeyboardRemove())
            await state.finish()
        elif message.text.lower() == 'назад':
            await bot.send_message(message.chat.id, 'Введите название карты(на английском)',
                                   reply_markup=ReplyKeyboardRemove())
            await FSMMap.previous()
        else:
            await bot.send_message(message.chat.id, 'я тебя не понял')

#@dp.message_handler()
async def start(message : types.Message):
    await bot.send_message(message.from_user.id, 'Привет')


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(cm_start, commands=['Карты'])
    dp.register_message_handler(map_n, state=FSMMap.map_id)
    dp.register_message_handler(t_s_map, state=FSMMap.team_solo_stats)
