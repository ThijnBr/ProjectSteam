import databaseConnection
import random
from datetime import datetime, timedelta

conn = databaseConnection.connect()

def voorspelFunctie(lst):
    gemiddelde = sum(lst)/len(lst)
    waarnemingen = 0
    for x in lst:
        waarnemingen += (x-gemiddelde)**2
    variantie = waarnemingen/len(lst)
    deviatie = variantie**0.5

    print(deviatie)

    lstrange = len(lst)
    for x in range(lstrange):
        newPoint = lst[(lstrange+x)//2] + random.uniform(0.0,deviatie)
        lst.append(newPoint)
    return lst
    

def getGamePlayers(appid, cursor):
    sql = f"SELECT time FROM concurrentPlayers WHERE gamesteam_appid = {appid} ORDER BY time ASC"
    sql2 = f"SELECT amount FROM concurrentPlayers WHERE gamesteam_appid = {appid}"
    cursor.execute(sql)
    timelist = cursor.fetchall()
    cursor.execute(sql2)
    amount = cursor.fetchall()

    newTime = []
    newAmount = []
    for x in range(len(timelist)):
        newTime.append(timelist[x][0])
        newAmount.append(amount[x][0])
    
    newAmount = voorspelFunctie(newAmount)

    timeRange = len(newTime)
    for x in range(timeRange-1):
        newTime.append(str(datetime.strptime(newTime[(timeRange+x)//2], "%m/%d/%y:%H:%M:%S") + timedelta(hours=1))+"voorspelling")
    return newTime, newAmount

def getAllChartData():
    cursor = conn.cursor()
    sql = "SELECT gamesteam_appid FROM concurrentPlayers LIMIT 20"
    cursor.execute(sql)
    data = cursor.fetchall()

    chart_data = []
    for x in data:
        sql2 = f"SELECT name FROM game WHERE steam_appid = {x[0]}"
        cursor.execute(sql2)
        name = cursor.fetchall()
        chart_data.append([getGamePlayers(x[0], cursor), name[0][0]])
    cursor.close()
    return chart_data

