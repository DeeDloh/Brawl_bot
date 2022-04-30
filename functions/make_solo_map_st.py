import requests
from PIL import Image



def image_braw_map(brawlers):

    map = Image.open('C:/Users/Kirill/Documents/GitHub/Brawl_bot/sample_solo_stats_3.png')

    for n in range(len(brawlers)):
        image = Image.open(requests.get(brawlers[n], stream=True).raw).resize((161, 161))
        if n < 5:
            map.paste(image, (69 + n * 225, 379))
        else:
            map.paste(image, (69 + (n - 5) * 225, 609))
    map.save(f'123.png')
    return f'123.png'
