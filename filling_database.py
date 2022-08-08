import requests
import pprint
import sqlite3

"""
all_map = requests.get('https://api.brawlapi.com/v1/maps').json()['list']
con = sqlite3.connect("brawl.db")
cursor = con.cursor()
for map in all_map:
    name = map['name']
    id = map['id']
    print(map)
    cursor.execute(f'''INSERT INTO id_brawlstars_map (name, id_brawl) VALUES ("{name}", {id})''')
con.commit()
"""

con = sqlite3.connect("brawl.db")
cursor = con.cursor()