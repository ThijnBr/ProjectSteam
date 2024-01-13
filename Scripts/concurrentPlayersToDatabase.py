import requests
from datetime import datetime
import time
import databaseConnection

conn = databaseConnection.connect()

def concurrentPlayersRequest():
    request = 'https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1/?'
    response = requests.get(request)
    return response.json()['response']['ranks']

def stringtodatetime(time_str):
    return datetime.strptime(time_str, "%m/%d/%y:%H:%M:%S")

def insertConcurrentPlayers(appid, amount, time):
    cursor = conn.cursor()
    checkSQL = 'SELECT time FROM concurrentPlayers WHERE gamesteam_appid = %s'
    cursor.execute(checkSQL, (appid,))
    lst = cursor.fetchall()
    
    insertSQL = "INSERT INTO concurrentPlayers (gamesteam_appid, amount, time) values (%s, %s, %s)"
    if len(lst) < 10:
        try:
            cursor.execute(insertSQL, (appid, amount, time))
        except:
            cursor.close()
    else:
        print('this')
        cursor.execute(insertSQL, (appid, amount, time))

        earliest_time = stringtodatetime(lst[0][0])
        for x in lst:
            if earliest_time > stringtodatetime(x[0]):
                earliest_time = stringtodatetime(x[0])

        earliest_time = earliest_time.strftime("%m/%d/%y:%H:%M:%S")
        deleteSQL = 'DELETE FROM concurrentPlayers WHERE gamesteam_appid = %s AND time = %s'

        cursor.execute(deleteSQL, (appid, str(earliest_time)))

    conn.commit()
    cursor.close()

def getConcurrentPlayers():
    data = concurrentPlayersRequest()
    now = datetime.now()

    current_time = now.strftime("%D:%H:%M:%S")
    for x in data:
        appid = x['appid']
        currentPlayers = x['concurrent_in_game']
        insertConcurrentPlayers(appid, currentPlayers, current_time)

    

def executeFunction():
    while True:
        now = datetime.now()
        if now.hour in list(range(0,24)) and now.minute in list(range(0,60)):
            getConcurrentPlayers()
            print('executed')

        time.sleep(5)

executeFunction()
    
