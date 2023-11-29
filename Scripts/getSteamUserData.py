import requests

apikey = '14B0152189C811A5DE80FE50EB4DA7CC'
steamID = 76561198401205997

def getFriendUserIDs(steamid):
    apilink = f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={apikey}&steamid={steamid}&relationship=friend'
    data = requests.get(apilink)
    jsonData = data.json()
    playerIDs = ''
    for playerID in jsonData['friendslist']['friends']:
        playerIDs += ','+playerID['steamid']
    return playerIDs

def getFriendSummary(steamIDs):
    apilink =  f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={apikey}&steamids={steamIDs}'
    data = requests.get(apilink)
    jsonData = data.json()
    return jsonData

print(getFriendSummary(getFriendUserIDs(steamID)))

