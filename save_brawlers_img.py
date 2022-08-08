import requests

all_brawlers = requests.get('https://api.brawlapi.com/v1/brawlers').json()['list']
for brawler in all_brawlers:
    img = brawler['imageUrl2']
    p = requests.get(img)
    out = open(f"./avatar_brawlers/{brawler['id']}.jpg", "wb")
    out.write(p.content)
    out.close()
