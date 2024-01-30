import requests
from . import normalDescription

def getGameNews(game_id):
    request = f'https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={game_id}&count=5&format=json'
    response = requests.get(request)
    data = response.json()
    list = []
    for x in data['appnews']['newsitems']:
        contents = normalDescription.getNormalDescription(x['contents'])
        list.append((x['title'],contents))
    return list