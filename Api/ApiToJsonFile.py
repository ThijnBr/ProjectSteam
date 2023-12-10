import requests
import pandas as pd

apiUrl = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json"
data = requests.get(apiUrl)
jsonData = data.json()
df = pd.DataFrame(jsonData)
df.to_json(r'C:\Users\jacob\source\repos\ThijnBr\ProjectSteam\ApiCsv\gameIds.json')