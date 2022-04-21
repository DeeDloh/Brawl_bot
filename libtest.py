from brawlstats import Client
import requests
from pprint import pprint
from urllib.request import urlopen

bs = Client('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImFiZTNkMjYyLWRlM2MtNGJlMC1hMGQzLThkNTNlMWU2NWRjMCIsImlhdCI6MTY1MDU3MTU4Miwic3ViIjoiZGV2ZWxvcGVyL2U2MTYyMDE4LTkyNjAtYmI1NC1lZmFjLTYyOTUyMGRkM2FlYiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMzcuMTQ1LjIxMC4xMDAiLCI5NS4yNy4xNDMuMTA5Il0sInR5cGUiOiJjbGllbnQifV19.P1d3ehUHBa2ND5-0rhtapGMHCh3wbLAOX0AALXMl3ZRccRhiOZ6kES_0wYImjkHfDBpSNrLCUX0DsEYES5F5Ow')
player = bs.get_player('#8GVQPJV')
icons = requests.get('https://api.brawlapi.com/v1/icons').json()

icon_id = str(player.icon['id'])
icon_url = icons['player'][icon_id]['imageUrl']
print(icon_url)
with open('mma_icon.png', 'wb') as img:
    img.write(requests.get(icon_url).content)
