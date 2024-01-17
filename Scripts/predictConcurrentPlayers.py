import databaseConnection
import random
from datetime import datetime, timedelta

conn = databaseConnection.connect()

def calculateGraph(yList):
    num_iterations = 10000
    learning_rate = 0.0001
    a, b = 0, 0

    lst = []
    for x in range(len(yList)):
        lst.append((x,yList[x]))

    for _ in range(num_iterations):
        for point in lst:
            x, y = point
            error = (a + b * x)- y
            a = a - error * learning_rate
            b = b - x * error * learning_rate
    return a, b

def predict(a, b, x):
    return a + b * x

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
    
    a, b = calculateGraph(newAmount)

    predictLine = []
    for x in range(len(newAmount)):
        predictLine.append(predict(a,b,x))

    timeRange = len(newTime)
    for x in range(timeRange-1):
        newTime.append('')
    return newTime, newAmount, predictLine, b

def getAllChartData():
    cursor = conn.cursor()
    sql = """SELECT gamesteam_appid, SUM(amount) AS total_amount
                FROM concurrentPlayers
                GROUP BY gamesteam_appid
                ORDER BY total_amount DESC LIMIT 10"""
    cursor.execute(sql)
    data = cursor.fetchall()

    chart_data = []
    for x in data:
        sql2 = f"SELECT name, header_image FROM game WHERE steam_appid = {x[0]}"
        cursor.execute(sql2)
        name = cursor.fetchall()
        chart_data.append([getGamePlayers(x[0], cursor), name[0][0], name[0][1]])
    cursor.close()
    return chart_data

