import pandas as pd
import requests
import time

import os
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

gameIdLocation = r'gameIds.json'
df = pd.read_json(gameIdLocation)

def getGameDetailsApi(gameId):
    apiUrl = f'http://store.steampowered.com/api/appdetails?appids={gameId}'
    data = requests.get(apiUrl)
    return data.json()

def insertGameDetailsJson(record):
    df = pd.DataFrame(record)
    return df.to_json(r"gameDetail.json", mode='a', lines=True, orient='records', indent=2, index=False)    

def getGameDetails(df):
    numRows = len(df["applist"]["apps"])
    currentRow = 41
    for row in range(currentRow, numRows):
        gameId = df["applist"]["apps"][row]["appid"]
        gameDetail= getGameDetailsApi(gameId)
        print(gameId)
        
        try:
            if str(gameDetail[str(gameId)]) != 'null':
                if str(gameDetail[str(gameId)]['success']) == 'True' and str(gameDetail[str(gameId)]['data']['type']) == 'game':
                    # print(gameDetail)
                    insertGameDetailsJson(gameDetail)
        except:
            with open ('errorIds.json', 'a')as f:
                f.write(str(gameId)+',')
            print('error')
        currentRow += 1
        print(currentRow)
    print("It's done!!!")
getGameDetails(df)