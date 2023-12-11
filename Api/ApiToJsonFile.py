import requests
import pandas as pd

df = pd.read_csv(r"C:\Users\jacob\source\repos\ThijnBr\ProjectSteam\Api\ApiKeys.csv")
apikey = df.iloc[0, 1]

apiUrl = (
    f"http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key={apikey}&format=json"
)
data = requests.get(apiUrl)
jsonData = data.json()
df = pd.DataFrame(jsonData)
df.to_json(r"C:\Users\jacob\source\repos\ThijnBr\ProjectSteam\Api\gameIds.json")