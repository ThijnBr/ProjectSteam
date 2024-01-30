from . import databaseConnection as db
from . import normalDescription
from . import gamesToDatabase
import asyncio

async def getLibraryGames(steam_ids):
    conn = db.connect()
    cursor = conn.cursor()

    # Dynamically create placeholders for steam_ids in the SQL query
    placeholders = ', '.join(['%s'] * len(steam_ids))
    sql = f"""SELECT name, header_image, detailed_description, steam_appid 
              FROM game 
              WHERE steam_appid IN ({placeholders});"""

    # Use the steam_ids directly as values
    values = tuple(steam_ids)
    cursor.execute(sql, values)
    library_games = cursor.fetchall()

    data = []
    if library_games:
        for game in library_games:
            if len(game) > 2:
                html_description = normalDescription.getNormalDescription(game[2])
                game_data = (game[0], game[1], html_description, game[3])
                data.append(game_data)
            else:
                data.append(game)

    cursor.close()
    conn.close()

    return data

def getDetailedGames(steam_id):
    if steam_id == 'True':
        return
    conn = db.connect()
    cursor = conn.cursor()

    sql = """SELECT name, header_image, detailed_description, release_date, price, developer, requirements.pc, requirements.mac, requirements.linux, Windows, platforms.Mac, platforms.Linux FROM game
            JOIN requirements ON steam_appid = gamesteam_appid
            JOIN platforms on steam_appid = platforms.gamesteam_appid
            WHERE steam_appid = %s"""

    cursor.execute(sql, (steam_id,))
    LibraryGames = cursor.fetchall()

    data = []
    if LibraryGames:
        sql2 = "SELECT path_full FROM screenshot WHERE gamesteam_appid = %s"
        cursor.execute(sql2, (steam_id,))
        screenshot = cursor.fetchall()

        screenshots = []
        for x in screenshot:
            screenshots.append(x[0])
        for x in range(len(LibraryGames[0])):
            if x == 2 or x==6 or x==7 or x==8:
                html = normalDescription.getNormalDescription(LibraryGames[0][x])
                data.append(html)
            else:
                data.append(LibraryGames[0][x])
        data.append(screenshots)
        data.append(f'https://store.steampowered.com/app/{steam_id}/')
    else:
        gamesToDatabase.idsToDatabase([steam_id], None, None) 

    cursor.close()
    conn.close()

    return data

