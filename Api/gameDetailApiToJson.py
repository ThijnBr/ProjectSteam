import pandas as pd
import requests
import time

gameIdLocation = r'C:\Users\jacob\source\repos\ThijnBr\ProjectSteam\Api\gameIds.json'
df = pd.read_json(gameIdLocation)

def getGameDetailsApi(gameId):
    apiUrl = f'http://store.steampowered.com/api/appdetails?appids={gameId}'
    data = requests.get(apiUrl)
    return data.json()

def insertGameDetailsJson(record):
    df = pd.DataFrame(record)
    return df.to_json(r"C:\Users\jacob\source\repos\ThijnBr\ProjectSteam\Api\gameDetail.json", mode='a', lines=True, orient='records', indent=2, index=False)    

def getGameDetails(df):
    numRows = len(df["applist"]["apps"])
    for row in range(numRows):
        gameId = df["applist"]["apps"][row]["appid"]
        gameDetail= getGameDetailsApi(gameId)
        print(gameId)
        
        if str(gameDetail[str(gameId)]) != 'null':
            if str(gameDetail[str(gameId)]['success']) == 'True' and str(gameDetail[str(gameId)]['data']['type']) == 'game':
                # print(gameDetail)
                insertGameDetailsJson(gameDetail)
                time.sleep(1.5)
    print("It's done!!!")
getGameDetails(df)