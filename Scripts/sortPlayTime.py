import databaseConnection

con = databaseConnection.connect()

def selectPlayTime(con):
    cursor = con.cursor()
    cursor.execute("select gamesteam_appid, SUM(playtimelast2weeks), steamusersteamid from playtime group by gamesteam_appid, steamusersteamid")
    return cursor.fetchall()

playerTimeList = selectPlayTime(con)

def insertion_sort(arr):
    for i in range(1, len(arr)):
        j=i
        while arr[j-1][1] < arr[j][1] and j > 0:
            arr[j-1], arr[j] = arr[j], arr[j-1]
            j-=1
    return arr