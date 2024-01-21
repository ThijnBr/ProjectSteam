from multiprocessing.reduction import duplicate
import databaseConnection
import getSteamUserFriends
import getSteamUserGameData

con = databaseConnection.connect()

import asyncio


def getPlayTime(steamID):
    friendIdList = getSteamUserFriends.getFriendUserIDs(steamID)

    friend_games_data = asyncio.run(
        getSteamUserGameData.get_friend_games_async(friendIdList)
    )

    gamesList = []

    for friend_id, data in zip(friendIdList, friend_games_data):
        if data is not None and "response" in data and "games" in data["response"]:
            games = data["response"]["games"]
            friend_games = []

            for game in games:
                try:
                    gameId = game.get("appid")
                    playtime_2weeks = int(game.get("playtime_2weeks", 0))
                    if playtime_2weeks == 0:
                        continue
                    friend_games.append([gameId, playtime_2weeks])
                except (KeyError, ValueError):
                    continue

            if friend_games:
                gamesList.append([friend_id, friend_games])

    return gamesList

def findOriginalIndex(stringArr, keyString): 
    for i in range(len(stringArr)):
        for j in range(len(stringArr[i])):
            # print(stringArr[i][j])
            if stringArr[i][j] == keyString:
                return i
 

def combineGamePlaytime(steamID):
    playtimeList = getPlayTime(steamID)
    duplicatesdictSum = {}

    for i in playtimeList:
        for j in range(len(i[1])):             
            gameId = i[1][j][0]
            playTime = i[1][j][1]
            
            if gameId in duplicatesdictSum:
                duplicatesdictSum[gameId] += playTime
            else:
                duplicatesdictSum[gameId] = playTime

    return [[playTime, duplicatesdictSum[playTime]] for playTime in duplicatesdictSum]

def insertion_sort(arr):
    for i in range(1, len(arr)):
        j = i

        while arr[j - 1][1] < arr[j][1] and j > 0:
            arr[j - 1], arr[j] = arr[j], arr[j - 1]
            j -= 1
    return arr

print(insertion_sort(combineGamePlaytime(76561198401205997)))
