import databaseConnection

chart_data = [
        [['Label1', 'Label2', 'Label3'], [10, 20, 30]],
        [['Label1', 'Label2', 'Label3'], [15, 25, 35]],
    ]

conn = databaseConnection.connect()

def voorspelFunctie():
    

def getGamePlayers(appid, cursor):
    sql = f"SELECT time FROM concurrentPlayers WHERE gamesteam_appid = {appid} LIMIT 2"
    sql2 = f"SELECT amount FROM concurrentPlayers WHERE gamesteam_appid = {appid} LIMIT 2"
    cursor.execute(sql)
    timelist = cursor.fetchall()
    cursor.execute(sql2)
    amount = cursor.fetchall()

    newTime = []
    newAmount = []
    for x in range(len(timelist)):
        newTime.append(timelist[x][0])
        newAmount.append(amount[x][0])
    return newTime, newAmount

def getAllChartData():
    cursor = conn.cursor()
    sql = "SELECT gamesteam_appid FROM concurrentPlayers LIMIT 2"
    cursor.execute(sql)
    data = cursor.fetchall()

    chart_data = []
    for x in data:
        chart_data.append(getGamePlayers(x[0], cursor))
    cursor.close()
    return chart_data

