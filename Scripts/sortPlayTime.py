from .  import databaseConnection
from . import getSteamUserFriends
from . import getSteamUserGameData
from . import normalDescription
import asyncio

#returns a gameList [friendid,[gameid,playtime last 2 weeks]]
#async function to improve speed
def getPlayTime(steamID):
    #Deze functie verwijst naar het ophalen van Ids van je vrienden op Steam
    friendIdList = getSteamUserFriends.getFriendUserIDs(steamID)

    #Deze functie verwijst naar het ophalen van de gamedata van je vrienden op Steam
    friend_games_data = asyncio.run(
        getSteamUserGameData.get_friend_games_async(friendIdList)
    )

    gamesList = []
    #Dit gedeelte haalt alleen de playtime van de afgelopen 2 weken uit de opgehaalde gamedata
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

#returns playtime from all players combined per game.
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

#sort playtime from high to low with merge sort. returns a max of 6 games.
def mergeSort(arr):
    # Check if the length of the array is less than or equal to 1
    # If so, it's already sorted, so return the array
    if len(arr) <= 1:
        return arr

    # Split the array into two halves
    leftArray = arr[:len(arr)//2]  # Left half
    rightArray = arr[len(arr)//2:]  # Right half

    # Recursively call mergeSort on each half
    leftArray = mergeSort(leftArray)
    rightArray = mergeSort(rightArray)

    sortedArray = []

    # checks index for the left and right arrays
    i = 0
    j = 0

    # Compare elements from left and right arrays and merge them in sorted order
    while i < len(leftArray) and j < len(rightArray):
        if leftArray[i][1] > rightArray[j][1]:  # Compare based on the second element of each item
            sortedArray.append(leftArray[i])
            i += 1
        else:
            sortedArray.append(rightArray[j])
            j += 1
    
    # Append remaining elements from left array, if any are left
    while i < len(leftArray):
        sortedArray.append(leftArray[i])
        i += 1

    # Append remaining elements from right array, if any are left
    while j < len(rightArray):
        sortedArray.append(rightArray[j])
        j += 1

    # Return the sorted array with a limit of 6 elements
    return sortedArray[0:6]
    
#get name image link and description from database
def getGameDatabase(lst):
    conn = databaseConnection.connect()
    cursor = conn.cursor()
    game_data = []
    for x in lst:
        sql = f"SELECT name, header_image, detailed_description FROM game WHERE steam_appid = %s"
        cursor.execute(sql, (x[0], ))
        data = cursor.fetchall()
        game_data.append([data[0][0], data[0][1], normalDescription.getNormalDescription(data[0][2])])
    cursor.close()
    return game_data