from aiogram import Dispatcher, types
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from keyboards import kb_ts, kb_menu, kb_back
from functions import image_solo_braw_map, image_team_braw_map, image_showdown_solo_braw_map,\
    image_showdown_duo_braw_map
from functions import make_player_card
import requests
import os

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

    if mod_com == 'team':
        uni_stats = list(sorted(map['teamStats'], key=lambda x: x['data']['winRate']))[::-1]
        for com in range(len(uni_stats)):
            temp_spis = []
            if str(uni_stats[com]['brawler1']) in uni_braw:
                uni_braw[str(uni_stats[com]['brawler1'])] += 1
            else:
                uni_braw[str(uni_stats[com]['brawler1'])] = 1

            if str(uni_stats[com]['brawler2']) in uni_braw:
                uni_braw[str(uni_stats[com]['brawler2'])] += 1
            else:
                uni_braw[str(uni_stats[com]['brawler2'])] = 1

            if str(uni_stats[com]['brawler3']) in uni_braw:
                uni_braw[str(uni_stats[com]['brawler3'])] += 1
            else:
                uni_braw[str(uni_stats[com]['brawler3'])] = 1

            if com < 4:
                str_vivod += f'{", ".join(uni_stats[com]["hash"].split("+"))}\nWin Rate: {str(uni_stats[com]["data"]["winRate"])[:5]}\n\n'

            for j in range(1, 4):
                k = uni_stats[com][f'brawler{j}']
                id_braw = requests.get(f'https://api.brawlapi.com/v1/brawlers/{k}').json()['imageUrl2']
                temp_spis.append(id_braw)
            brawlers.append(temp_spis)
    else:

        stats = list(sorted(map['stats'], key=lambda x: x['winRate']))[-10:][::-1]
        uni_stats = list(sorted(map['teamStats'], key=lambda x: x['data']['winRate']))[::-1]
        for com in range(len(uni_stats)):
            if str(uni_stats[com]['brawler1']) in uni_braw:
                uni_braw[str(uni_stats[com]['brawler1'])] += 1
            else:
                uni_braw[str(uni_stats[com]['brawler1'])] = 1

            if str(uni_stats[com]['brawler2']) in uni_braw:
                uni_braw[str(uni_stats[com]['brawler2'])] += 1
            else:
                uni_braw[str(uni_stats[com]['brawler2'])] = 1

            if str(uni_stats[com]['brawler3']) in uni_braw:
                uni_braw[str(uni_stats[com]['brawler3'])] += 1
            else:
                uni_braw[str(uni_stats[com]['brawler3'])] = 1

        for i in range(len(stats)):
            brawler = requests.get(f'https://api.brawlapi.com/v1/brawlers/{stats[i]["brawler"]}').json()
            brawlers.append(brawler['imageUrl2'])
            if i < 5:
                str_vivod += f'{brawler["name"]}\nWin Rate: {str(stats[i]["winRate"])[:5]}\n\n'
    braw_uni = list(sorted(list(uni_braw.items()), key=lambda x: x[1])[::-1])[0][0]
    vivod = requests.get(f'https://api.brawlapi.com/v1/brawlers/{braw_uni}').json()['name']
    str_vivod = f'Универсальный игрок:\n{vivod}\n\n{str_vivod}'
    return (str_vivod, brawlers, braw_uni)

def stats_showdown_solo_map_get(id_map):
    map = requests.get(f'https://api.brawlapi.com/v1/maps/{id_map}').json()
    str_vivod = ''
    brawlers = []
    stats = list(sorted(map['stats'], key=lambda x: x['winRate']))[-10:][::-1]
    for i in range(len(stats)):
        brawler = requests.get(f'https://api.brawlapi.com/v1/brawlers/{stats[i]["brawler"]}').json()
        brawlers.append(brawler['imageUrl2'])
        if i < 8:
            str_vivod += f'{brawler["name"]}\nWin Rate: {str(stats[i]["winRate"])[:5]}\n\n'
    return (str_vivod, brawlers)

def stats_showdown_duo_map_get(id_map):
    map = requests.get(f'https://api.brawlapi.com/v1/maps/{id_map}').json()
    str_vivod = ''
    brawlers = []
    uni_stats = list(sorted(map['teamStats'], key=lambda x: x['data']['winRate']))[::-1]
    uni_braw = {}
    for com in range(len(uni_stats)):
        temp_spis = []
        if str(uni_stats[com]['brawler1']) in uni_braw:
            uni_braw[str(uni_stats[com]['brawler1'])] += 1
        else:
            uni_braw[str(uni_stats[com]['brawler1'])] = 1

        if str(uni_stats[com]['brawler2']) in uni_braw:
            uni_braw[str(uni_stats[com]['brawler2'])] += 1
        else:
            uni_braw[str(uni_stats[com]['brawler2'])] = 1


        if com < 4:
            str_vivod += f'{", ".join(uni_stats[com]["hash"].split("+"))}\nWin Rate: {str(uni_stats[com]["data"]["winRate"])[:5]}\n\n'

        for j in range(1, 3):
            k = uni_stats[com][f'brawler{j}']
            id_braw = requests.get(f'https://api.brawlapi.com/v1/brawlers/{k}').json()['imageUrl2']
            temp_spis.append(id_braw)
        brawlers.append(temp_spis)
    braw_uni = list(sorted(list(uni_braw.items()), key=lambda x: x[1])[::-1])[0][0]
    vivod = requests.get(f'https://api.brawlapi.com/v1/brawlers/{braw_uni}').json()['name']
    str_vivod = f'Универсальный игрок:\n{vivod}\n\n{str_vivod}'
    return (str_vivod, brawlers, braw_uni)


class FSMMap(StatesGroup):
    map_id = State()
    team_solo_stats = State()


#@dp.message_handler(commands='Карты')
async def cm_start(message : types.Message):
    await FSMMap.map_id.set()
    await bot.send_message(message.chat.id, 'Введите название карты (на английском)', reply_markup=kb_back)


#@dp.message_handler(state=FSMMap.map_id)
async def map_n(message : types.Message, state : FSMContext):
    if message.text.lower() == 'назад':
        await bot.send_message(message.chat.id, 'НАЗАД', reply_markup=kb_menu)
        await state.finish()
    else:
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
    await bot.send_message(message.chat.id, 'Подожди немного', reply_markup=ReplyKeyboardRemove())
    msg = message.text
    async with state.proxy() as data:
        if msg.lower() in ['тим', 'соло']:
            if msg.lower() == 'тим':
                data['team_solo_stats'] = 'team'
            else:
                data['team_solo_stats'] = 'solo'
            if len(data['map_id']) == 1:
                inf = stats_map_get(data['map_id'][0], data['team_solo_stats'])
                if data['team_solo_stats'] == 'solo':
                    img_name = image_solo_braw_map(inf[1], inf[2], data['map_id'])
                    path_img = open(img_name, 'rb')
                else:
                    img_name = image_team_braw_map(inf[1], inf[2], data['map_id'])
                    path_img = open(img_name, 'rb')
                await bot.send_photo(chat_id=message.chat.id, photo=path_img, caption=inf[0],
                                     reply_markup=kb_menu)
                os.remove(img_name)
            else:
                if data['team_solo_stats'] == 'solo':
                    mode = requests.get(f'https://api.brawlapi.com/v1/maps/{data["map_id"][0]}').json()['gameMode'][
                        'name']
                    if mode == 'Solo Showdown':
                        inf = stats_showdown_solo_map_get(data['map_id'][0])
                        img_name = image_showdown_solo_braw_map(inf[1], ['map_id'][0])
                    else:
                        inf = stats_showdown_solo_map_get(data['map_id'][1])
                        img_name = image_showdown_solo_braw_map(inf[1], data['map_id'][1])
                    path_img = open(img_name, 'rb')
                    await bot.send_photo(chat_id=message.chat.id, photo=path_img, caption=inf[0],
                                         reply_markup=kb_menu)
                else:
                    mode = requests.get(f'https://api.brawlapi.com/v1/maps/{data["map_id"][0]}').json()['gameMode'][
                        'name']
                    if mode == 'Duo Showdown':
                        inf = stats_showdown_duo_map_get(data['map_id'][0])
                        img_name = image_showdown_duo_braw_map(inf[1], inf[2], data['map_id'][0])
                    else:
                        inf = stats_showdown_duo_map_get(data['map_id'][1])
                        img_name = image_showdown_duo_braw_map(inf[1], inf[2], data['map_id'][1])

                    path_img = open(img_name, 'rb')
                    await bot.send_photo(chat_id=message.chat.id, photo=path_img, caption=inf[0],
                                         reply_markup=kb_menu)
                    os.remove(img_name)
            await state.finish()
        elif msg.lower() == 'назад':
            await bot.send_message(message.chat.id, 'Введите название карты(на английском)',
                                   reply_markup=kb_menu)
            await FSMMap.previous()
        else:
            await bot.send_message(message.chat.id, 'я тебя не понял')


#---------------------------------------------------------------


#-----------------------------Игрок-----------------------------
class FSMPlayer(StatesGroup):
    playertag = State()

# @dp.message_handler(commands='player')
async def getting_playertag(message: types.Message):
    await FSMPlayer.playertag.set()
    await bot.send_message(message.chat.id, 'Введите тэг игрока (регистр и решётка не важны)', reply_markup=kb_back)


# @dp.message_handler(state=FSMPlayer.playertag)
async def give_player_stats(message : types.Message, state: FSMContext):
    card_making = make_player_card(message.text)
    if message.text.lower() == 'назад':
        await bot.send_message(message.chat.id, 'НАЗАД', reply_markup=kb_menu)
        await state.finish()
    elif card_making == 0:
        await bot.send_message(message.chat.id, 'Некорректный тэг!')
    else:
        player_in_kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('График изменения кол-ва трофеев',
                                                                                  callback_data='send_graph'))
        await bot.send_photo(chat_id=message.chat.id, photo=open(card_making, 'rb'), reply_markup=player_in_kb)
        os.remove(card_making)
        await state.finish()


# @dp.callback_query_handler(text='send_graph', state=FSMPlayer.playertag)
async def send_graph(callback : types.CallbackQuery):
    await callback.message.answer_photo(photo=open(requests.get('https://share.brawlify.com/player-graph/' + FSMPlayer.playertag.state, stream=True).raw, 'rb'))
    await callback.answer()

#---------------------------------------------------------------


#-----------------------------Клубы-----------------------------

#---------------------------------------------------------------




#@dp.message_handler(commands=['start'])
async def start(message : types.Message):
    text = 'Бот по статистике в Бравл Старс\nКоманды:\n/start, /help, /map, /player\nSupport @lDeeDl @pom_dorka'
    await bot.send_message(message.from_user.id, text, reply_markup=kb_menu)

#@dp.message_handler()
async def all_msg(message : types.Message):
    msg = message.text
    if msg.lower() == 'карта':
        await cm_start(message)
    elif msg.lower() == 'игрок':
        await getting_playertag(message)
    else:
        await bot.send_message(message.chat.id, 'Я тебя не понял', reply_markup=kb_menu)


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(cm_start, commands=['map'])
    dp.register_message_handler(map_n, state=FSMMap.map_id)
    dp.register_message_handler(t_s_map, state=FSMMap.team_solo_stats)
    dp.register_message_handler(getting_playertag, commands=['player'])
    dp.register_message_handler(give_player_stats, state=FSMPlayer.playertag)
    dp.register_message_handler(all_msg)
    dp.register_callback_query_handler(send_graph, state=FSMPlayer.playertag)
