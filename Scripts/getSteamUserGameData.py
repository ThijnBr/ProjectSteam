import requests
import pandas as pd
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)


def getFriendGames(steamID):
    df = pd.read_csv('..\Api\ApiKeys.csv')
    apikey = df.iloc[0, 1]
    url = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={apikey}&steamid={steamID}&format=json&include_appinfo=true'
    data = requests.get(url)
    return data.json()
    