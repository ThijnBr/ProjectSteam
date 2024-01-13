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
        if data[appid]['data']['type'] != 'game':
            delete_sql = f"""
                            DELETE FROM platforms WHERE gamesteam_appid = {appid};
                            DELETE FROM game_categorie WHERE gamesteam_appid = {appid};
                            DELETE FROM game_genre WHERE gamesteam_appid = {appid};
                            DELETE FROM requirements WHERE gamesteam_appid = {appid};
                            DELETE FROM screenshot WHERE gamesteam_appid = {appid};
                            DELETE FROM support_info WHERE gamesteam_appid = {appid};
                            DELETE FROM game WHERE steam_appid = {appid};"""
        else:
            try:
                discount = data[appid]['data']['price_overview']['discount_percent']
            except (KeyError, TypeError):
                discount = 'NULL'
            update_sql = f"UPDATE game SET discount = {discount} WHERE steam_appid = {appid};"
    except:
        continue

    cursor = conn.cursor()
    
    if data[appid]['data']['type'] != 'game':
        cursor.execute(delete_sql)
    else:
        cursor.execute(update_sql)
    
    conn.commit()
    cursor.close()
    
    row += 1
    time.sleep(1.5)
