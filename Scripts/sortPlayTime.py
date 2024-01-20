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

def findIndex(stringArr, keyString):
    result = []
 
    for i in range(len(stringArr)):
 
        for j in range(len(stringArr[i])):
            if stringArr[i][j] == keyString:
                result.append(i)
                result.append(j)
                return result
    result.append(-1)
    result.append(-1)
    
    return result
 

def combineGamePlaytime(steamID):
    playtimeList = getPlayTime(steamID)

    savedGames = []
    duplicatesTotal = []
    for i in playtimeList:
        print(i)
        for j in range(len(i[1])):
            # print(i[1][j][0])
            # print(i[1][j][1])
            gameId = i[1][j][0]
            
            #Als je een duplicant plaats de gameId in een lijst en in die lijst zet je weer een lijst waarin alle playtimes zitten die bij de gameId horen, bijvoorbeeld: [4000[29, 69]]. 
            #Maak dan de sum() van duplicateList, bijvoorbeeld: sum(duplicates[i][1])
            #Vervang de sum met de lijst op positie een
            #Denk na over wat te doen met originele lijst en de duplicates

            #Deze if zoekt of gameId in de 2d lijst zit van savedgames, zoja; slaat op in lijst duplicates
            # if savedGames and any(gameId in x for x in savedGames):
            #     #probleem met lijst duplicates, is tijd moet bij elkaar opgeteld 
            #     print("test")
            #     indexDupecate = findIndex(savedGames, gameId)
            #     duplicatesTotal.append([gameId, savedGames[indexDupecate][1]])
            #     print(duplicatesTotal)
            # elif gameId not in savedGames:
            #     savedGames.append([i[1][j][0], i[1][j][1]])
            #     # print("testElse")
    
    return savedGames

def insertion_sort(arr):
    for i in range(1, len(arr)):
        j = i
        while arr[j - 1][1][0] < arr[j][1][0] and j > 0:
            arr[j - 1], arr[j] = arr[j], arr[j - 1]
            j -= 1
    return arr


combineGamePlaytime(76561198401205997)