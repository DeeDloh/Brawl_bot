# from create_bot import bs
from PIL import Image, ImageDraw, ImageFont
from brawlstats import Client
import string
from requests import get as reqget
from os.path import abspath
from os import sep as ossep

bs = Client('СВОЙ КЛЮЧ')


def make_player_card(playertag):
    playertag = playertag.upper() if playertag[0] == '#' else '#' + playertag.upper()
    player = bs.get_player(playertag)  # берём из API объект игрока
    icons = reqget('https://api.brawlapi.com/v1/icons').json()  # берем из другого API .json-файл со всеми иконками

    en_font_path = abspath('../fonts/english.ttf').replace(ossep, '/')  # в этом абзаце готовим шрифты
    ru_font_path = abspath('../fonts/russian.ttf').replace(ossep, '/')
    check_name_lang = player.name.translate(str.maketrans('', '', string.punctuation)).lower()  # выбираем, какой шрифт
    check_name_lang = check_name_lang.translate(str.maketrans('', '', string.digits))           # использовать для ника
    if len(set(check_name_lang + string.ascii_lowercase)) == len(string.ascii_lowercase):       # в зависимости от языка
        name_font = ImageFont.truetype(en_font_path, size=56, encoding='unic')
    else:
        name_font = ImageFont.truetype(ru_font_path, size=48, encoding='unic')
    tag_font = ImageFont.truetype(en_font_path, size=18, encoding='unic')  # остальные шрифты всегда английские
    stats_font = ImageFont.truetype(en_font_path, size=26, encoding='unic')

    card = Image.open('../player_card_base.png')  # открываем основу для карточки игрока
    draw = ImageDraw.Draw(card)

    try:
        avatar = Image.open(reqget(icons['player'][str(player.icon['id'])]['imageUrl'], stream=True).raw)  # загружаем аватарку
        card.paste(avatar.resize((150, 150)), (30, 30, 180, 180))  # рисуем аватарку
    except KeyError:  # API с иконками неофициальное, иконки могут добавляться с задержкой
        pass
    draw.text((202, 28), player.name, font=name_font, fill='#' + player.name_color[4:])  # рисуем ник игрока
    draw.text((202, 99), playertag, font=tag_font, fill='#6C757D')  # рисуем тэг игрока

    card.save(f'player_{playertag[1:]}.png')


make_player_card(input())