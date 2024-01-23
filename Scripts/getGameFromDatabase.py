import databaseConnection as db

def getLibraryGames(name):
    conn = db.connect()
    cursor = conn.cursor()

    sql = f"SELECT header_image, name FROM game WHERE name "
    cursor.execute(sql)

    names = cursor.fetchall()

    cursor.close()
    conn.close()

    return names
