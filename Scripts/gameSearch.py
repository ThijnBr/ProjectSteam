from . import databaseConnection as db

def getGames(name):
    conn = db.connect()
    cursor = conn.cursor()

    sql = f"SELECT header_image FROM game WHERE REPLACE(LOWER(name), '®', '') ILIKE '%{name}%' LIMIT 10"
    cursor.execute(sql)

    names = cursor.fetchall()

    cursor.close()
    conn.close()

    return names

# conn = db.connect()
# def getGames():
#     cursor = conn.cursor()

#     sql = f"SELECT name FROM game"
