import requests

apikey = '14B0152189C811A5DE80FE50EB4DA7CC'
# steamID = 76561198401205997

#sort Friends on playing game -> online -> Offline
def sortFriends(lst):
    
    for i in range(len(lst)):
        minindex = i
        for j in range(i+1, len(lst)):
            info = lst[j]['info']
            if info != 'Online' and info != 'Offline' or (info == 'Online' and lst[minindex]['info'] == 'Offline'):
                minindex = j
        lst[minindex], lst[i] = lst[i], lst[minindex]

    print(lst)
    
    return lst

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
def getFriendSummary(steamID):
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

def getFriendsData(steamID):
    friendList = getFriendSummary(steamID)
    players = []
    for x in friendList['response']['players']:
        
        name = x['personaname']
        avatar = x['avatarmedium']
        state = x['personastate']
        if state != 0:
            try:
                info = 'Playing '+x['gameextrainfo']
            except KeyError:
                info = 'Online'
        else:
            info = 'Offline'
        players.append(playerDictionary(name,avatar,info))
    sorted = sortFriends(players)
    return sorted

