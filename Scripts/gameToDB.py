import pandas as pd
import requests

gameIdLocation = r'C:\Users\jacob\source\repos\ThijnBr\ProjectSteam\Api\gameIds.json'
df = pd.read_json(gameIdLocation)

def getGameDetailApi(gameId):
    apiUrl = f'http://store.steampowered.com/api/appdetails?appids={gameId}'
    data = requests.get(apiUrl)
    return data.json()

def insertGameDetails():
    pass

def getGameDetails(df):
    
    # print(df.to_string())
    numRows = len(df["applist"]["apps"])
    gameDetailsList = []
    
    for row in range(numRows):
        gameId = df["applist"]["apps"][row]["appid"]
        gameDetailsList.append(getGameDetailApi(gameId))
        print(gameDetailsList[row][str(gameId)]['data']['type'])
        
        if gameDetailsList[row][str(gameId)]['data']['type'] == 'game':    
            insertGameDetails()
            gameDetailsList[row][str(gameId)]['data']['name']    

getGameDetails(df)

