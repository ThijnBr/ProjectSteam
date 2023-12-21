import requests
import pandas as pd
import getSteamUserFriends

import os

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

df = pd.read_csv('..\Api\ApiKeys.csv')
apikey = df.iloc[0, 1]

steamID = 76561198401205997
friendIds = getSteamUserFriends.getFriendUserIDs(steamID)
print(friendIds)

