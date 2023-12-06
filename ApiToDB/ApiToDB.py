import requests
import pandas as pd

applink = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json"
data = requests.get(applink)
jsonDataFrame = data.json()
jsonData = pd.read_json(jsonDataFrame)
print(type(jsonData))
file = ('C:/Users/jacob/source/repos/ThijnBr/ProjectSteam/ApiCsv/gameIds.csv')


dict = {
        'appid': [],
        'name': []
        }
df = pd.DataFrame(dict)
print(df)
df.to_csv(file, mode = 'w', index=False)
