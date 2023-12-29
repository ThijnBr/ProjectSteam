import pandas as pd
import getSteamUserFriends
import getSteamUserGameData
import os
import databaseConnection

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

df = pd.read_csv('..\Api\ApiKeys.csv')
apikey = df.iloc[0, 1]

conn = databaseConnection.connect()

# steamID = 76561198401205997

import asyncio

def getPlayTime(steamID):
    api_key = '14B0152189C811A5DE80FE50EB4DA7CC'  # Replace with your API key
    friendIdList = getSteamUserFriends.getFriendUserIDs(steamID)
    
    loop = asyncio.get_event_loop()
    friend_games_data = loop.run_until_complete(getSteamUserGameData.get_friend_games_async(friendIdList, api_key))

    gamesList = []

    for friend_id, data in zip(friendIdList, friend_games_data):
        if data is not None and 'response' in data and 'games' in data['response']:
            games = data['response']['games']
            friend_games = []

            for game in games:
                try:
                    gameId = game.get('appid')
                    playtime_2weeks = int(game.get('playtime_2weeks', 0))
                    friend_games.append([gameId, playtime_2weeks])
                except (KeyError, ValueError):
                    continue
            
            if friend_games:
                gamesList.append([friend_id, friend_games])
    
    return gamesList
               
def insertQueries(playtime, gameid, userid):
    userid = str(userid)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM steamuser WHERE steamid = %s", (userid,))
    user_exists = cursor.fetchone()

    if not user_exists:
        cursor.execute("INSERT INTO steamuser VALUES (%s)", (userid,))
        print(f"User with usersteamid {userid} inserted into the User table.")
    sql = "DELETE FROM playtime WHERE steamusersteamid = %s"
    cursor.execute(sql, (userid,))
    sql = "INSERT INTO playtime values (%s, %s, %s)"
    cursor.execute(sql,(playtime, gameid,userid))

def insertToDatabase(lst):
    for x in lst:  
        playtime = x[1][0][1]
        gameid = x[1][0][0]
        userid = x[0]
        insertQueries(playtime, gameid, userid)

insertToDatabase(getPlayTime(76561198401205997))
conn.commit()


# def insertion_sort(arr):
#     for i in range(1, len(arr)):
#         current = arr[i]
#         j = i - 1

#         while j >= 0 and arr[j][1] < current[1]:
#             arr[j + 1] = arr[j]
#             j -= 1

#         arr[j + 1] = current

#     return arr


# sorted_data = insertion_sort(getPlayTime())
# print(sorted_data)