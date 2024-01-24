import databaseConnection as db
import normalDescription

def getLibraryGames(steam_id):
    conn = db.connect()
    cursor = conn.cursor()

    sql = """SELECT name, header_image, detailed_description, release_date, price, developer FROM game WHERE steam_appid = %s;
            SELECT pc, mac, linux FROM requirements WHERE gamesteam_appid = %s;
            SELECT path_full FROM Screenshot WHERE gamesteam_appid = %s;
            SELECT Windows, Mac, Linux FROM Platforms WHERE gamesteam_appid = %s;"""

    values = (steam_id,)
    cursor.execute(sql, values)
    LibraryGames = cursor.fetchall()

    data = []
    for x in range(len(LibraryGames[0])):
        if x == 2:
            html = normalDescription.getNormalDescription(LibraryGames[0][x])
            data.append(html)
        else:
            data.append(LibraryGames[0][x])
    cursor.close()
    conn.close()

    return data

def getDetailedGames(steam_id):
    conn = db.connect()
    cursor = conn.cursor()

    sql = """SELECT name, header_image, detailed_description, release_date, price, developer, requirements.pc, requirements.mac, requirements.linux, path_full, Windows, platforms.Mac, platforms.Linux FROM game
            JOIN requirements ON steam_appid = gamesteam_appid
            JOIN screenshot ON steam_appid = screenshot.gamesteam_appid
            JOIN platforms on steam_appid = platforms.gamesteam_appid
            WHERE steam_appid = %s"""

    cursor.execute(sql, (steam_id,))
    LibraryGames = cursor.fetchall()

    data = []
    for x in range(len(LibraryGames[0])):
        if x == 2 or x==6 or x==7 or x==8:
            html = normalDescription.getNormalDescription(LibraryGames[0][x])
            data.append(html)
        else:
            data.append(LibraryGames[0][x])

    cursor.close()
    conn.close()

    return data

