import requests

import pandas as pd

df = pd.read_csv('..\ApiCsv\ApiKeys.csv')
apikey = df.iloc[0, 1]

steamID = None

apilink = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={apikey}&steamid={steamID}&format=json&include_appinfo=true'