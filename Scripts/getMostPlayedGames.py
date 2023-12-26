import pandas as pd
import getSteamUserFriends
import getSteamUserGameData
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

df = pd.read_csv('..\Api\ApiKeys.csv')
apikey = df.iloc[0, 1]

steamID = 76561198401205997
friendIdList = getSteamUserFriends.getFriendUserIDs(steamID)

def getPlayTime():
    gamesList = []
    playtimeList = []
    appidList = []
    for x in range(2):
        gamesList.append(getSteamUserGameData.getFriendGames(friendIdList[x]))
        # print(f"{friendIdList[x]} \n {gamesList[x]}\n")
        for j in range(gamesList[x]['response']['game_count']-1):    
            playtimeList.append(f"{gamesList[x]['response']['games'][j]['appid']}, {gamesList[x]['response']['games'][j]['playtime_forever']}")
        
    return playtimeList
def sortPlayeTime():
    for x in getPlayTime():
    
#Bij het opvragen van de games kijk welke game de hoogste playtimeforever en kijk dan of zij in de afgelopen 2 weken die game hebben gespeelt

