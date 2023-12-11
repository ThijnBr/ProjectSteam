import pandas as pd
import requests
import time

gameIdLocation = r'C:\Users\jacob\source\repos\ThijnBr\ProjectSteam\Api\gameIds.json'
df = pd.read_json(gameIdLocation)

def getGameDetailApi(gameId):
    apiUrl = f'http://store.steampowered.com/api/appdetails?appids={gameId}'
    data = requests.get(apiUrl)
    return data.json()

def insertGameDetails():
    pass

def getGameDetails(df):
    numRows = len(df["applist"]["apps"])
    gameDetailsList = []
    for row in range(numRows):
        gameId = df["applist"]["apps"][row]["appid"]
        gameDetailsList.append(getGameDetailApi(gameId))
        print(f"{gameId} {gameDetailsList[row][str(gameId)]['success']}")
        time.sleep(1)
        if gameDetailsList[row][str(gameId)]['success'] == 'True':
            print('success == true')    
            if gameDetailsList[row][str(gameId)]['data']['type'] == 'game':
                print('Game == true')
                insertGameDetails()
                gameDetailsList[row][str(gameId)]['data']['name']

getGameDetails(df)