from . import databaseConnection as db
from . import normalDescription
from . import gamesToDatabase
import asyncio

async def getLibraryGames(steam_id, time=0):
    conn = db.connect()
    cursor = conn.cursor()

    sql = """SELECT name, header_image, detailed_description, steam_appid FROM game WHERE steam_appid = %s;"""

    values = (steam_id,)
    cursor.execute(sql, values)
    LibraryGames = cursor.fetchall()

    data = []
    if LibraryGames:
        for x in range(len(LibraryGames[0])):
            if x == 2:
                html = normalDescription.getNormalDescription(LibraryGames[0][x])
                data.append(html)
            else:
                data.append(LibraryGames[0][x])
    elif time==0:
        gamesToDatabase.idsToDatabase([steam_id], None, None)
        return await getLibraryGames(steam_id, 1)       

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
    if LibraryGames:
        for x in range(len(LibraryGames[0])):
            if x == 2 or x==6 or x==7 or x==8:
                html = normalDescription.getNormalDescription(LibraryGames[0][x])
                data.append(html)
            else:
                data.append(LibraryGames[0][x])
    else:
        gamesToDatabase.idsToDatabase([steam_id], None, None) 

    cursor.close()
    conn.close()

    return data

