from aiogram import Dispatcher, types
from create_bot import bot, dp, cursor
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
    map_id = cursor.execute(f'SELECT id_brawl FROM id_brawlstars_map WHERE name = "{map_name}"').fetchall()
    map_id = [i[0] for i in map_id][:2]
    return map_id


def stats_map_get(id_map, mod_com):
    map = requests.get(f'https://api.brawlapi.com/v1/maps/{id_map}').json()
    str_vivod = ''
    brawlers = []
    universal_braw = {}

    if mod_com == 'team':
        universal_stats = list(sorted(map['teamStats'], key=lambda x: x['data']['winRate']))[::-1]
        for com in range(len(universal_stats)):
            temp_spis = []
            if str(universal_stats[com]['brawler1']) in universal_braw:
                universal_braw[str(universal_stats[com]['brawler1'])] += 1
            else:
                universal_braw[str(universal_stats[com]['brawler1'])] = 1

            if str(universal_stats[com]['brawler2']) in universal_braw:
                universal_braw[str(universal_stats[com]['brawler2'])] += 1
            else:
                universal_braw[str(universal_stats[com]['brawler2'])] = 1

            if str(universal_stats[com]['brawler3']) in universal_braw:
                universal_braw[str(universal_stats[com]['brawler3'])] += 1
            else:
                universal_braw[str(universal_stats[com]['brawler3'])] = 1

            if com < 4:
                name = ", ".join(universal_stats[com]["hash"].split("+"))
                str_vivod += f'{name}\nWin Rate: {str(universal_stats[com]["data"]["winRate"])[:5]}\n\n'

            for j in range(1, 4):
                id_braw = universal_stats[com][f'brawler{j}']
                temp_spis.append(id_braw)
            brawlers.append(temp_spis)
    else:

        stats = list(sorted(map['stats'], key=lambda x: x['winRate']))[-10:][::-1]
        universal_stats = list(sorted(map['teamStats'], key=lambda x: x['data']['winRate']))[::-1]
        for com in range(len(universal_stats)):
            if str(universal_stats[com]['brawler1']) in universal_braw:
                universal_braw[str(universal_stats[com]['brawler1'])] += 1
            else:
                universal_braw[str(universal_stats[com]['brawler1'])] = 1

            if str(universal_stats[com]['brawler2']) in universal_braw:
                universal_braw[str(universal_stats[com]['brawler2'])] += 1
            else:
                universal_braw[str(universal_stats[com]['brawler2'])] = 1

            if str(universal_stats[com]['brawler3']) in universal_braw:
                universal_braw[str(universal_stats[com]['brawler3'])] += 1
            else:
                universal_braw[str(universal_stats[com]['brawler3'])] = 1

        for i in range(len(stats)):
            brawler = requests.get(f'https://api.brawlapi.com/v1/brawlers/{stats[i]["brawler"]}').json()
            id_braw = stats[i]["brawler"]
            brawlers.append(id_braw)
            if i < 5:
                str_vivod += f'{brawler["name"]}\nWin Rate: {str(stats[i]["winRate"])[:5]}\n\n'
    braw_universal = list(sorted(list(universal_braw.items()), key=lambda x: x[1])[::-1])[0][0]
    vivod = requests.get(f'https://api.brawlapi.com/v1/brawlers/{braw_universal}').json()['name']
    str_vivod = f'Универсальный игрок:\n{vivod}\n\n{str_vivod}'
    return (str_vivod, brawlers, braw_universal)


def stats_showdown_solo_map_get(id_map):
    map = requests.get(f'https://api.brawlapi.com/v1/maps/{id_map}').json()
    str_vivod = ''
    brawlers = []
    stats = list(sorted(map['stats'], key=lambda x: x['winRate']))[-10:][::-1]
    for i in range(len(stats)):
        brawler = requests.get(f'https://api.brawlapi.com/v1/brawlers/{stats[i]["brawler"]}').json()
        id_braw = stats[i]["brawler"]
        brawlers.append(id_braw)
        if i < 8:
            str_vivod += f'{brawler["name"]}\nWin Rate: {str(stats[i]["winRate"])[:5]}\n\n'
    return (str_vivod, brawlers)


def stats_showdown_duo_map_get(id_map):
    map = requests.get(f'https://api.brawlapi.com/v1/maps/{id_map}').json()
    str_vivod = ''
    brawlers = []
    universal_stats = list(sorted(map['teamStats'], key=lambda x: x['data']['winRate']))[::-1]
    universal_braw = {}
    for com in range(len(universal_stats)):
        temp_spis = []
        if str(universal_stats[com]['brawler1']) in universal_braw:
            universal_braw[str(universal_stats[com]['brawler1'])] += 1
        else:
            universal_braw[str(universal_stats[com]['brawler1'])] = 1

        if str(universal_stats[com]['brawler2']) in universal_braw:
            universal_braw[str(universal_stats[com]['brawler2'])] += 1
        else:
            universal_braw[str(universal_stats[com]['brawler2'])] = 1

        if com < 4:
            name = ", ".join(universal_stats[com]["hash"].split("+"))
            str_vivod += f'{name}\nWin Rate: {str(universal_stats[com]["data"]["winRate"])[:5]}\n\n'

        for j in range(1, 3):
            id_braw = universal_stats[com][f'brawler{j}']
            temp_spis.append(id_braw)
        brawlers.append(temp_spis)
    braw_universal = list(sorted(list(universal_braw.items()), key=lambda x: x[1])[::-1])[0][0]
    vivod = requests.get(f'https://api.brawlapi.com/v1/brawlers/{braw_universal}').json()['name']
    str_vivod = f'Универсальный игрок:\n{vivod}\n\n{str_vivod}'
    return (str_vivod, brawlers, braw_universal)


class FSMMap(StatesGroup):
    map_id = State()
    team_solo_stats = State()


# @dp.message_handler(commands='Карты')
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
                        img_name = image_showdown_solo_braw_map(inf[1], data['map_id'][0])

                    else:
                        inf = stats_showdown_solo_map_get(data['map_id'][1])
                        img_name = image_showdown_solo_braw_map(inf[1], data['map_id'][1])

                    path_img = open(img_name, 'rb')
                    await bot.send_photo(chat_id=message.chat.id, photo=path_img, caption=inf[0],
                                         reply_markup=kb_menu)
                    os.remove(img_name)

                else:
                    mode = requests.get(f'https://api.brawlapi.com/v1/maps/{data["map_id"][0]}').json()['gameMode'][
                        'name']
                    if mode == 'Duo Showdown':
                        inf = stats_showdown_duo_map_get(data['map_id'][0])
                        img_name = image_showdown_duo_braw_map(inf[1], inf[2], data['map_id'][0])
                        print(inf[1], inf[2], data['map_id'][0])
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
    url = 'https://share.brawlify.com/player-graph/' + FSMPlayer.playertag.state
    await callback.message.answer_photo(photo=open(requests.get(url, stream=True).raw, 'rb'))
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
        b = "\n".join(['Bea, Griff, Janet', 'Win Rate: 100'])
        answer_1 = f'''Универсальный игрок:\nBea\n{b}\t{b}'''
        with open('./html_templates/solo_template.html', mode='r') as f:
            answer = '\n'.join(f.readlines())
        await bot.send_message(message.chat.id, answer, reply_markup=kb_menu, parse_mode="HTML")


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(cm_start, commands=['map'])
    dp.register_message_handler(map_n, state=FSMMap.map_id)
    dp.register_message_handler(t_s_map, state=FSMMap.team_solo_stats)
    dp.register_message_handler(getting_playertag, commands=['player'])
    dp.register_message_handler(give_player_stats, state=FSMPlayer.playertag)
    dp.register_message_handler(all_msg)
    dp.register_callback_query_handler(send_graph, state=FSMPlayer.playertag)
