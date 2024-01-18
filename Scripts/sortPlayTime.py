import databaseConnection
import getSteamUserFriends
import getSteamUserGameData

con = databaseConnection.connect()

import asyncio

def getPlayTime(steamID):
    friendIdList = getSteamUserFriends.getFriendUserIDs(steamID)
    
    friend_games_data = asyncio.run(getSteamUserGameData.get_friend_games_async(friendIdList))

    gamesList = []

    for friend_id, data in zip(friendIdList, friend_games_data):
        if data is not None and 'response' in data and 'games' in data['response']:
            games = data['response']['games']
            friend_games = []

            for game in games:
                try:
                    gameId = game.get('appid')
                    playtime_2weeks = int(game.get('playtime_2weeks', 0))
                    if playtime_2weeks == 0:
                        continue
                    friend_games.append([gameId, playtime_2weeks])
                except (KeyError, ValueError):
                    continue
            
            if friend_games:
                gamesList.append([friend_id, friend_games])
    
    return gamesList

def combineGamePlaytime():
    

def insertion_sort(arr):
    for i in range(1, len(arr)):
        j=i
        while arr[j-1][1] < arr[j][1] and j > 0:
            arr[j-1], arr[j] = arr[j], arr[j-1]
            j-=1
    return arr