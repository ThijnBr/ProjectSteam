import requests

apikey = '14B0152189C811A5DE80FE50EB4DA7CC'
steamID = 76561198401205997

#get user ids of friends
def getFriendUserIDs(steamid):
    apilink = f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={apikey}&steamid={steamid}&relationship=friend'
    data = requests.get(apilink)
    jsonData = data.json()
    playerIDs = ''
    for playerID in jsonData['friendslist']['friends']:
        playerIDs += ','+playerID['steamid']
    return playerIDs

#json data of all friends
def getFriendSummary():
    steamIDs = getFriendUserIDs(steamID)
    apilink =  f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={apikey}&steamids={steamIDs}'
    data = requests.get(apilink)
    jsonData = data.json()
    return jsonData

#json structure for friend data
def playerDictionary(name, avatar, info):
    return      {
        'name' : name,
        'avatar': avatar,
        'info': info
    }

#getting friends online
def FriendsOnline():
    friendList = getFriendSummary()
    players = []
    for x in friendList['response']['players']:
        state = x['personastate']
        if state != 0:
            name = x['personaname']
            avatar = x['avatarmedium']
            try:
                info = x['gameextrainfo']
            except KeyError:
                info = 'Online'
            players.append(playerDictionary(name,avatar,info))
    return players

#get which friends are offline
def FriendsOffline():
    friendList = getFriendSummary()
    players = []
    for x in friendList['response']['players']:
        state = x['personastate']
        if state == 0:
            name = x['personaname']
            avatar = x['avatarmedium']
            info = 'Offline'
            players.append(playerDictionary(name,avatar,info))
    return players

