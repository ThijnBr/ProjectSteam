import databaseConnection
import requests
import os
import time

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

conn = databaseConnection.connect()

def getGameIds():
    cursor = conn.cursor()
    sql = 'SELECT steam_appid FROM game'
    cursor.execute(sql)
    gameids = cursor.fetchall()
    id_list = [str(x[0]) for x in gameids]
    cursor.close()
    return id_list

def makeRequest(appid):
    request_url = f'http://store.steampowered.com/api/appdetails?appids={appid}'
    response = requests.get(request_url)
    return response.json()

gameIds = getGameIds()

row = 0
for appid in gameIds:
    print(row)
    print(appid)
    data = makeRequest(appid)
    try:
        discount = data[appid]['data']['price_overview']['discount_percent']
    except (KeyError, TypeError):
        discount = 'NULL'

    cursor = conn.cursor()
    update_sql = f"UPDATE game SET discount = {discount} WHERE steam_appid = {appid};"
    cursor.execute(update_sql)
    conn.commit()
    cursor.close()
    row += 1
    time.sleep(1.5)