import requests
from PIL import Image


def image_solo_braw_map(brawlers, uni_brawler):
    map = Image.open('./sample_solo_stats_3.png')
    link_image = requests.get(f'https://api.brawlapi.com/v1/brawlers/{uni_brawler}').json()['imageUrl2']
    image_uni = Image.open(requests.get(link_image, stream=True).raw).resize((251, 251))
    map.paste(image_uni, (475, 55))
    for n in range(len(brawlers)):
        image = Image.open(requests.get(brawlers[n], stream=True).raw).resize((161, 161))
        if n < 5:
            map.paste(image, (69 + n * 225, 379))
        else:
            map.paste(image, (69 + (n - 5) * 225, 609))
    map.save(f'123.png')
    return f'123.png'


def image_team_braw_map(brawlers, uni_brawler):
    map = Image.open('./sample_team_stats.png')
    link_image = requests.get(f'https://api.brawlapi.com/v1/brawlers/{uni_brawler}').json()['imageUrl2']
    image_uni = Image.open(requests.get(link_image, stream=True).raw).resize((250, 250))
    map.paste(image_uni, (475, 55))
    for n in range(len(brawlers)):
        for k in range(3):
            image = Image.open(requests.get(brawlers[n][k], stream=True).raw).resize((70, 70))
            map.paste(image, (65 + k * 80 + (n % 4) * 280, 395 + (n // 4) * 130))
    map.save(f'123.png')
    return f'123.png'