import json
import databaseConnection

import os

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

conn = databaseConnection.connect()

jsonValues = ['steam_appid', 
              'name', 
              'required_age', 
              'is_free',
              'price_overview',
              'detailed_description', 
              'supported_languages', 
              'header_image', 
              'release_date', 
              'recommendations', 
              'developers', 
              'publishers', 
              'pc_requirements', 
              'mac_requirements',
              'linux_requirements',
              'platforms',
              'categories',
              'genres',
              'screenshots',
              'support_info']

def getDescriptions():
    cursor = conn.cursor()
    sql = "SELECT id FROM categorie"
    cursor.execute(sql)
    descriptions = cursor.fetchall()
    list = []
    for x in descriptions:
        list.append(int(x[0]))
    cursor.close()
    return list

def getGenres():
    cursor = conn.cursor()
    sql = "SELECT id FROM genre"
    cursor.execute(sql)
    descriptions = cursor.fetchall()
    list = []
    for x in descriptions:
        list.append(int(x[0]))
    cursor.close()
    return list

descriptions = getDescriptions()
genres = getGenres()


# with open('correctData.json', 'r') as f:
#     data = json.load(f)

current = 0

def insertCategory(id, description):
    sql = "INSERT INTO categorie values (%s, %s)"
    cursor.execute(sql,(id,description))

def insertGameCategory(gameId, categorieId):
    sql = 'INSERT INTO game_categorie values (%s, %s)'
    cursor.execute(sql,(gameId, categorieId))

def insertGenre(id, description):
    sql = "INSERT INTO genre values (%s, %s)"
    cursor.execute(sql,(id,description))

def insertGameGenre(gameId, genreId):
    sql = 'INSERT INTO game_genre values (%s, %s)'
    cursor.execute(sql,(genreId, gameId))

def insertSupportinfo(dict, gameId):
    sql = 'INSERT INTO support_info values(%s, %s, %s)'
    url = dict['url']
    email = dict['email']
    cursor.execute(sql, (url, email, gameId))

def getValue(innerJson, arg, gameId):
    global descriptions
    global genres
    value = innerJson[arg]
    match arg:
        case 'release_date':
            return innerJson[arg]['date']
        case 'categories':
            for x in innerJson[arg]:
                id = x['id']
                desc = x['description']
                if id not in descriptions:
                    descriptions.append(id)
                    insertCategory(id, desc)
            return innerJson[arg]
        case 'genres':
            for x in innerJson[arg]:
                id = int(x['id'])
                desc = x['description']
                if id not in genres:
                    genres.append(id)
                    insertGenre(id, desc)
            return innerJson[arg]
        case 'developers':
            return value[0]
        case 'publishers':
            return value[0]
        case 'price_overview':
            return value['initial']
        case 'recommendations':
            return value['total']
        case _:
            return value

def insertGame(lst):
    sql = 'INSERT INTO game values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(sql, lst)

def insertRequirements(lst):
    sql = 'INSERT INTO requirements values (%s, %s, %s, %s)'
    cursor.execute(sql, lst)

def insertPlatforms(lst, gameId):
    sql = 'INSERT INTO platforms values(%s, %s, %s, %s)'
    windows = lst['windows']
    mac = lst['mac']
    linux = lst['linux']
    platforms = windows, mac, linux
    cursor.execute(sql, (*platforms, gameId))

def insertScreenshots(lst, gameId):
    sql = 'INSERT INTO screenshot values(%s, %s, %s, %s)'
    id = lst['id']
    path_thumbnail = lst['path_thumbnail']
    path_full = lst['path_full']
    cursor.execute(sql, (id, path_thumbnail, path_full, gameId))

row = 0
currentRow = row

with open('../gameIds.txt', 'r') as f:
    datax = f.read()
    datax = datax.replace('{', '')
    datax = datax.replace('}', '')
    datax = datax.replace(' ', '')
    data = datax.split(',')
    # print(data)

import requests
def getGameDetail(appid):
    data = requests.get(f'http://store.steampowered.com/api/appdetails?appids={appid}').json()
    try:
        data = list(data.values())[0]['data']
    except:
        print(data)
        return False
    
    return data
data = ['295110']
for x in range(row, len(data)):
    innerJson = getGameDetail(data[x])
    if innerJson == False:
        continue
    cursor = conn.cursor()
    gametoInsert = []
    categoriestoInsert = None
    requirementsToInsert = []
    platformstoInsert = None
    genrestoInsert = None
    screenshotsToInsert = None
    supportInfoToInsert = None
    dlcToInsert = None
    if isinstance(innerJson, bool):
        continue
    gameId = innerJson['steam_appid']
    gametoInsert.append(gameId)
    requirementsToInsert.append(gameId)
    currentGame = 0
    for x in jsonValues:
        currentGame += 1
        if x == 'steam_appid':
            continue
        try:
            value = getValue(innerJson, x, gameId)
        except Exception as e:
            value = None
        if currentGame < 13:
            gametoInsert.append(value)
        else:
            if x == 'categories':
                categoriestoInsert = value
            elif x == 'genres':
                genrestoInsert = value
            elif x == 'pc_requirements' or x == 'mac_requirements' or x == 'linux_requirements':
                if value == [] or value == None:
                    requirementsToInsert.append('')
                else:
                    requirementsToInsert.append(value['minimum'])
            elif x == 'platforms':
                platformstoInsert = value
            elif x == 'screenshots':
                screenshotsToInsert = value
            elif x == 'support_info':
                supportInfoToInsert = value

        # print(x, ' ', value)  
    # print(gametoInsert)
    try:
        insertGame(gametoInsert)
        if requirementsToInsert != None:
            insertRequirements(requirementsToInsert)
        insertPlatforms(platformstoInsert, gameId)
        insertSupportinfo(supportInfoToInsert, gameId)
        if categoriestoInsert != None:
            for x in categoriestoInsert:
                insertGameCategory(gameId, x['id'])
        if genrestoInsert != None:
            for x in genrestoInsert:
                insertGameGenre(gameId, x['id'])
        if screenshotsToInsert != None:
            for x in screenshotsToInsert:
                insertScreenshots(x, gameId)
    except Exception as e:
        with open('ERRORDS.TXT', 'a', encoding='utf-8') as f:
            error = str(e) + ' with gameid ' + str(gameId) + '\n'
            f.write(error)

    currentRow += 1
    print(currentRow)
    cursor.close()
    conn.commit()
    
"""INSERT INTO categorie values (2, 'test');
INSERT INTO game values (10, 'test2', 0, False, 'nee', 'NL', 'ding', '2000', NULL, 't','f');
INSERT INTO game_categorie values (10, 2);"""