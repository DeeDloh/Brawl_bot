from aiogram import Dispatcher, types
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from keyboards import kb_ts
from functions.make_image_map_st import image_solo_braw_map, image_team_braw_map
import requests

#-----------------------------Карты-----------------------------


def find_map(map_name):
    all_map = requests.get('https://api.brawlapi.com/v1/maps').json()
    map_id = []
    for map in all_map['list']:
        if map_name == map['name']:
            map_id.append(map['id'])
    return map_id


def stats_map_get(id_map, mod_com):
    map = requests.get(f'https://api.brawlapi.com/v1/maps/{id_map}').json()
    str_vivod = ''
    brawlers = []
    uni_braw ={}
    uni_stats = list(sorted(map['teamStats'], key=lambda x: x['data']['winRate']))[::-1]
    for com in uni_stats:
        if str(com['brawler1']) in uni_braw:
            uni_braw[str(com['brawler1'])] += 1
        else:
            uni_braw[str(com['brawler1'])] = 1
            
        if str(com['brawler2']) in uni_braw:
            uni_braw[str(com['brawler2'])] += 1
        else:
            uni_braw[str(com['brawler2'])] = 1
            
        if str(com['brawler3']) in uni_braw:
            uni_braw[str(com['brawler3'])] += 1
        else:
            uni_braw[str(com['brawler3'])] = 1
            

    if mod_com == 'team':
        stats = uni_stats
        stats_solo = list(sorted(map['stats'], key=lambda x: x['winRate']))[-10:][::-1]
        for i in range(len(stats)):
            temp_spis = []
            if i < 10:
                brawler = requests.get(f'https://api.brawlapi.com/v1/brawlers/{stats_solo[i]["brawler"]}').json()
                str_vivod += f'{brawler["name"]}\nWin Rate: {str(stats_solo[i]["winRate"])[:5]}\n\n'
            for j in range(1, 4):
                k = stats[i][f'brawler{j}']
                id_braw = requests.get(f'https://api.brawlapi.com/v1/brawlers/{k}').json()['imageUrl2']
                temp_spis.append(id_braw)
            brawlers.append(temp_spis)

    else:
        stats = list(sorted(map['stats'], key=lambda x: x['winRate']))[-10:][::-1]
        for i in range(len(stats)):
            brawler = requests.get(f'https://api.brawlapi.com/v1/brawlers/{stats[i]["brawler"]}').json()
            brawlers.append(brawler['imageUrl2'])
            str_vivod += f'{brawler["name"]}\nWin Rate: {str(stats[i]["winRate"])[:5]}\n\n'
    return (str_vivod, brawlers, list(sorted(uni_braw, key=lambda x: x[1]))[0])


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
        await bot.send_message(message.chat.id, 'Введите название карты(на английском)',
                               reply_markup=ReplyKeyboardRemove())
    async with state.proxy() as data:
        k = find_map(message.text)
        if k == []:
            await bot.send_message(message.chat.id, 'Такой карты нет')
        else:
            data['map_id'] = k
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
            if len(data['map_id']) == 1:
                inf = stats_map_get(data['map_id'][0], data['team_solo_stats'])
                if data['team_solo_stats'] == 'solo':
                    path_img = open(image_solo_braw_map(inf[1], inf[2]), 'rb')
                else:
                    path_img = open(image_team_braw_map(inf[1], inf[2]), 'rb')
                await bot.send_photo(chat_id=message.chat.id, photo=path_img, caption=inf[0],
                                     reply_markup=ReplyKeyboardRemove())
            await state.finish()
        elif message.text.lower() == 'назад':
            await bot.send_message(message.chat.id, 'Введите название карты(на английском)',
                                   reply_markup=ReplyKeyboardRemove())
            await FSMMap.previous()
        else:
            await bot.send_message(message.chat.id, 'я тебя не понял')


#---------------------------------------------------------------


#-----------------------------Игрок-----------------------------

#---------------------------------------------------------------


#-----------------------------Клубы-----------------------------

#---------------------------------------------------------------




#@dp.message_handler()
async def start(message : types.Message):
    await bot.send_message(message.from_user.id, 'Привет')

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(cm_start, commands=['maps'])
    dp.register_message_handler(map_n, state=FSMMap.map_id)
    dp.register_message_handler(t_s_map, state=FSMMap.team_solo_stats)