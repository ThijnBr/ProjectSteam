import requests
import databaseConnection

conn = databaseConnection.connect()


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
        if discountPct != 0:
            query = f'SELECT header_image, name FROM game WHERE steam_appid = {x}'
            cursor.execute(query)
            image = cursor.fetchone()
            print(image)
            wishlist.append((x,discountPct, image))

    cursor.close()
    return wishlist

def getSalesInPopular():
    cursor = conn.cursor()
    sql = """SELECT gamesteam_appid, SUM(amount) AS total_amount
                FROM concurrentPlayers
                GROUP BY gamesteam_appid
                ORDER BY total_amount DESC"""
    cursor.execute(sql)
    data = cursor.fetchall()

    popular = []
    for x in data:
        sql2 = f"SELECT discount, name, header_image FROM game WHERE steam_appid = {x[0]} AND CAST(discount AS INT) > CAST(0 AS INT);"

        cursor.execute(sql2)
        name = cursor.fetchall()
        if name == []:
            continue
        else:
            popular.append(name[0])
    cursor.close()
    return popular
    
