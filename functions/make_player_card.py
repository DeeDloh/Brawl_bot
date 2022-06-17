from create_bot import bs
from PIL import Image, ImageDraw, ImageFont
from brawlstats import Client
from requests import get as reqget
from os.path import abspath
from os import sep as ossep
from functions.is_english import is_english
from functions.end_of_season import trophies_statpoints_calc


def make_player_card(playertag):
    playertag = playertag.upper() if playertag[0] == '#' else '#' + playertag.upper()
    try:
        player = bs.get_player(playertag)  # берём из API объект игрока
    except Exception:
        return 0
    icons = reqget('https://api.brawlapi.com/v1/icons').json()  # берем из другого API .json-файл со всеми иконками

    en_font_path = abspath('./fonts/english.ttf').replace(ossep, '/')  # в этом абзаце готовим шрифты
    ru_font_path = abspath('./fonts/russian.ttf').replace(ossep, '/')
    if is_english(player.name):       # выбираем, какой шрифт использовать для ника в зависимости от языка
        name_font = ImageFont.truetype(en_font_path, size=56, encoding='unic')
    else:
        name_font = ImageFont.truetype(ru_font_path, size=48, encoding='unic')
    tag_font = ImageFont.truetype(en_font_path, size=18, encoding='unic')  # остальные шрифты всегда английские
    stats_font = ImageFont.truetype(en_font_path, size=26, encoding='unic')

    card = Image.open('./templates/player_card_base.png').convert("RGBA")  # открываем основу для карточки игрока
    draw = ImageDraw.Draw(card)

    try:
        avatar = Image.open(reqget(icons['player'][str(player.icon['id'])]['imageUrl'], stream=True).raw)  # загружаем аватарку
        card.paste(avatar.resize((150, 150)), (30, 30, 180, 180))  # отображаем аватарку
    except KeyError:  # API с иконками неофициальное, иконки могут добавляться с задержкой
        pass
    if player.name_color:
        draw.text((202, 28), player.name, font=name_font, fill='#' + player.name_color[4:])  # отображаем ник игрока
    else:
        draw.text((202, 28), player.name, font=name_font, fill='#ffffff')  # по какой-то причине, если ник игкрока белый, api вообще не возвращет пункт с цветом ника, вместо того чтоб вернуть "#ffffff". это очень тупо
    draw.text((202, 99), playertag, font=tag_font, fill='#6C757D')  # отображаем тэг игрока

    if player.club:  # отображаем название клуба, в котором находится игрок
        if is_english(player.club.name):  # выбираем, какой шрифт использовать для названия клуба в зависимости от языка
            club_font = stats_font
        else:
            club_font = ImageFont.truetype(ru_font_path, size=26, encoding='unic')
        draw.text((216, 282), player.club.name, font=club_font, fill='#f4801f', anchor='mm')
        club_icon = Image.open(reqget(icons['club'][str(player.get_club().badgeId)]['imageUrl'], stream=True).raw).resize((45, 50)).convert("RGBA")
        card.paste(club_icon, (39, 254), club_icon)
    else:  # если игрок не в клубе, то вместо названия отображаем надпись "Не в клубе"
        no_club_font = ImageFont.truetype(ru_font_path, size=26, encoding='unic')
        draw.text((216, 282), 'Не в клубе', font=no_club_font, fill='#6c757d', anchor='mm')

    draw.text((130, 406), str(player.trophies), font=stats_font, fill='#fec107', anchor='mm')  # отображаем кол-во кубков
    draw.text((300, 406), str(player.highest_trophies), font=stats_font, fill='#a5a5a5', anchor='mm')  # отображаем наивысшее кол-во кубков, которое когда-либо было у игрока
    draw.text((411, 405), str(player.exp_level), font=stats_font, fill='#ffffff', anchor='mm')  # отображаем уровень игрока
    draw.text((130, 523), str(player.x3vs3_victories), font=stats_font, fill='#cd0067', anchor='mm')  # отображаем кол-во побед 3 на 3
    draw.text((300, 523), str(player.solo_victories), font=stats_font, fill='#329900', anchor='mm')  # отображаем кол-во соло побед
    draw.text((470, 523), str(player.duo_victories), font=stats_font, fill='#329900', anchor='mm')  # отображаем отображаем кол-во дуо побед

    brawlers = player.brawlers
    trophies_loss, starpoints = trophies_statpoints_calc(player.trophies, brawlers)  # считаем и отображаем кол-во трофеев и звёздных очков после конца сезона
    draw.text((130, 640), str(trophies_loss), font=stats_font, fill='#fec107', anchor='mm')
    draw.text((300, 640), str(starpoints), font=stats_font, fill='#cb5bff', anchor='mm')
    draw.text((485, 640), f'{len(brawlers)}/{len(bs.get_brawlers().raw_data)}', font=stats_font, fill='#1aa6f5', anchor='mm')  # отображаем кол-во разблокированных игроком бравлеров

    path = f'player_{playertag[1:]}.png'
    card.save(path)  # сохраняем изображение
    return path


if __name__ == '__main__':
    make_player_card(input())