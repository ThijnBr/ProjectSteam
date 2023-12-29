import databaseConnection
import requests

conn = databaseConnection.connect()

def getGameIds():
    cursor = conn.cursor()
    sql = "SELECT steam_appid FROM game"
    cursor.execute(sql)
    descriptions = cursor.fetchall()
    game_ids = [x[0] for x in descriptions]
    cursor.close()
    return game_ids

def getSteamAppIDsFromAPI():
    url = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=YOUR_KEY&format=json'
    data = requests.get(url).json()
    if 'applist' in data and 'apps' in data['applist']:
        return [app['appid'] for app in data['applist']['apps']]
    return []

gameIds = getGameIds()
steam_app_ids = getSteamAppIDsFromAPI()

# Find the differences between the Steam App IDs in the database and those from the API
different_app_ids = set(steam_app_ids) - set(gameIds)
# print("Different App IDs:")
# print(different_app_ids)
# print(len(different_app_ids))

with open('gameIds.txt', 'w') as f:
    f.write(str(different_app_ids))
