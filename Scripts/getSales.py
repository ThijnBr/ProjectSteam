import requests
import asyncio
from . import databaseConnection
from . import getGameFromDatabase
from . import normalDescription

conn = databaseConnection.connect()

#returns games on wishlist with a discountpercentage > 0
def getSalesOnWishlist(steamID):    
    cursor = conn.cursor()

    wishlistAPI = f'https://store.steampowered.com/wishlist/profiles/{steamID}/wishlistdata/?p=0'
    data = requests.get(wishlistAPI)
    jsonData = data.json()
    wishlist = []
    for x in jsonData:
        try:
            discountPct = jsonData[x]['subs'][0]['discount_pct']
        except:
            continue
        if discountPct != 0 and discountPct != None:
            details = asyncio.run(getGameFromDatabase.getLibraryGames([x]))
            wishlist.append((discountPct, details[0]))
    cursor.close()
    return wishlist

#check if there is a sale in a game from the concurrentPlayer database.
def getSalesInPopular():
    cursor = conn.cursor()
    sql = """SELECT gamesteam_appid, SUM(amount) AS total_amount
                FROM concurrentPlayers
                GROUP BY gamesteam_appid
                ORDER BY total_amount DESC"""
    cursor.execute(sql)
    data = cursor.fetchall()

    list = []
    for x in data:
        sql2 = f"SELECT discount, name, header_image, detailed_description FROM game WHERE steam_appid = {x[0]} AND CAST(discount AS INT) > CAST(0 AS INT);"

        cursor.execute(sql2)
        name = cursor.fetchall()
        innerList = []
        if name == []:
            continue
        
        for x in range(len(name[0])):
            if x == 3:
                innerList.append(normalDescription.getNormalDescription(name[0][x]))
            else:
                innerList.append(name[0][x])
        if innerList != []:
            list.append(innerList)

    cursor.close()
    return list
    
