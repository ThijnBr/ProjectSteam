import databaseConnection
from psycopg2.errors import IntegrityError
conn = databaseConnection.connect()

#creates points for line
def predict(a, b, x):
    return a + b * x

def getAB(appid):
    sql = f"SELECT a,b FROM graphRC WHERE GameSteam_appid = {appid}"
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    a = data[0][0]
    b = data[0][1]
    return a, b

def getPlayersGame(appid):
    sql = f"SELECT time FROM concurrentPlayers WHERE gamesteam_appid = {appid} ORDER BY time ASC LIMIT 96"
    sql2 = f"SELECT amount FROM concurrentPlayers WHERE gamesteam_appid = {appid} LIMIT 96"

    cursor = conn.cursor()
    cursor.execute(sql)
    timelist = cursor.fetchall()
    cursor.execute(sql2)
    amount = cursor.fetchall()

    newTime = []
    newAmount = []
    for x in range(len(timelist)):
        newTime.append(timelist[x][0])
        newAmount.append(amount[x][0])
    return newAmount, newTime

#get concurrentPlayers for the past 96 hours, returns date, player amount, points, richtingscoefficient
def getGamePlayers(appid):
    newAmount, newTime = getPlayersGame(appid)
    a, b = getAB(appid)

    predictLine = []
    for x in range(len(newAmount)):
        predictLine.append(predict(a,b,x))

    timeRange = len(newTime)
    for x in range(timeRange-1):
        newTime.append('')
    return newTime, newAmount, predictLine, b

def getConcurrentPlayersFromDatabase(web):
    cursor = conn.cursor()
    if web == False:
        limit = 100
    else:
        limit = 10
    sql = f"""SELECT gamesteam_appid, SUM(amount) AS total_amount
                FROM concurrentPlayers
                GROUP BY gamesteam_appid
                ORDER BY total_amount DESC LIMIT {limit}"""
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

#returns all chart data used in html. [[time, amount, linepoints, richtingscoeffienct,name, imagelink]]
def getAllChartData(data):
    cursor = conn.cursor()
    chart_data = []
    for x in data:
        sql2 = f"SELECT name, header_image FROM game WHERE steam_appid = {x[0]}"
        cursor.execute(sql2)
        name = cursor.fetchall()
        chart_data.append([getGamePlayers(x[0]), name[0][0], name[0][1]])
    cursor.close()
    return chart_data

#berekend richtingscofficient en startYPositie van lijn.
def calculateGraph(steamID):
    print('calculating')
    yList = getPlayersGame(steamID)[0]

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
    
    query_insert = "INSERT INTO graphRC (gamesteam_appid, a, b) VALUES (%s, %s, %s)"
    query_update = "UPDATE graphRC SET a = %s, b = %s WHERE gamesteam_appid = %s"

    cursor = conn.cursor()

    try:
        cursor.execute(query_insert, (steamID, a, b))
    except IntegrityError:
        conn.rollback()  # Roll back the transaction in case of an exception
        cursor.execute(query_update, (a, b, steamID))
    finally:
        cursor.close()
        conn.commit()

# data = getConcurrentPlayersFromDatabase()
# for x in data:
#     calculateGraph(x[0])




