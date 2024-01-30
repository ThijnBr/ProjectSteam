import requests
from datetime import datetime
import time
import databaseConnection
from predictConcurrentPlayers import getConcurrentPlayersFromDatabase, calculateGraph

#get current game players top 100
def concurrentPlayersRequest():
    request = 'https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1/?'
    response = requests.get(request)
    return response.json()['response']['ranks']

#sets string to datetime
def stringtodatetime(time_str):
    return datetime.strptime(time_str, "%m/%d/%y:%H:%M")

#insert return from concurrentPlayersRequest by given appid.
def insertConcurrentPlayers(appid, amount, time, conn):
    cursor = conn.cursor()
    checkSQL = 'SELECT time FROM concurrentPlayers WHERE gamesteam_appid = %s'
    cursor.execute(checkSQL, (appid,))
    lst = cursor.fetchall()
    
    insertSQL = "INSERT INTO concurrentPlayers (gamesteam_appid, amount, time) values (%s, %s, %s)"

    #96 is max data in database per game. when it exceeds the first inserted player amount is removed
    if len(lst) < 96:
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

        earliest_time = earliest_time.strftime("%m/%d/%y:%H:%M")
        deleteSQL = 'DELETE FROM concurrentPlayers WHERE gamesteam_appid = %s AND time = %s'

        cursor.execute(deleteSQL, (appid, str(earliest_time)))

    conn.commit()
    cursor.close()

#loop through appids and execute other functions.
def getConcurrentPlayers(conn):
    data = concurrentPlayersRequest()
    now = datetime.now()

    current_time = now.strftime("%D:%H:%M")
    for x in data:
        appid = x['appid']
        currentPlayers = x['concurrent_in_game']
        insertConcurrentPlayers(appid, currentPlayers, current_time, conn)

    
#every hour there is a check if getConcurrentPlayers need to be executed. Runs on server.
def executeFunction():
    while True:
        now = datetime.now()
        if now.hour in list(range(0,24)) and now.minute == 0:
            conn = databaseConnection.connect()
            getConcurrentPlayers(conn)
            data = getConcurrentPlayersFromDatabase(False, conn)
            for x in data:
                calculateGraph(x[0], conn)
            print('executed')
            conn.close()

        time.sleep(60)

executeFunction()
    
