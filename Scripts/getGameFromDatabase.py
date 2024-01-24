from . import databaseConnection as db
from . import normalDescription

def getLibraryGames(steam_id):
    conn = db.connect()
    cursor = conn.cursor()

    sql = f"SELECT name, header_image, detailed_description release_date FROM game WHERE steam_appid = %s"
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
