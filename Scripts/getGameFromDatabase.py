import databaseConnection as db

def getLibraryGames(steam_id):
    conn = db.connect()
    cursor = conn.cursor()

    sql = f"SELECT name, header_image FROM game WHERE steam_appid = %s"
    values = (steam_id,)
    cursor.execute(sql, values)
    LibraryGames = cursor.fetchall()
    cursor.close()
    conn.close()

    return LibraryGames
