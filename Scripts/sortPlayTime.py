import databaseConnection
import getSteamUserFriends
import getSteamUserGameData
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

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
    return arr[0:6]


def getGameDatabase(lst):
    conn = databaseConnection.connect()
    cursor = conn.cursor()
    game_data = []
    for x in lst:
        sql2 = f"SELECT name, header_image, detailed_description FROM game WHERE steam_appid = {x[0]}"
        cursor.execute(sql2)
        name = cursor.fetchall()
        print(name)
        game_data.append([name[0][0], name[0][1]])
    cursor.close()
    return game_data

# print(insertion_sort(combineGamePlaytime(76561198401205997)))

print(getGameDatabase(insertion_sort(combineGamePlaytime(76561198401205997))))