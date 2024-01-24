import pandas as pd
import requests
import time
import psycopg2

conn = psycopg2.connect(
    host="play.miningminigames.uk.to",
    database="Steam",
    user="postgres",
    password="sTEAM.pROJECT")

def getGameDetailApi(gameId):
    apiUrl = f'http://store.steampowered.com/api/appdetails?appids={gameId}'
    data = requests.get(apiUrl)
    return data.json()
    
def insertStatement(conn, gameData, gameId):
    pass
    base = gameData[gameId]["data"]
    steam_appid = gameId
    name = base["name"]
    required_age = base["required_age"]
    is_free = base["is_free"]
    detailed_description = base["detailed_description"]
    supported_languages = base["supported_languages"]
    header_image = base["header_image"]
    release_date = base["release_date"]
    recommendations = base["recommendation"]
    developer = base["developer"]
    publisher = base["publisher"]
    
    cursor = conn.cursor()
    sql = "INSERT INTO Steam (steam_appid, name, required_age, is_free, detailed_description, supported_languages, header_image, release_date, recommendations, developer, publisher) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,)"
    data = (steam_appid, name, required_age, is_free, detailed_description, supported_languages, header_image, release_date, recommendations, developer, publisher)
    cursor.execute(sql, data)

def selectGame(conn, gameId):
    cursor = conn.cursor()
    sql = "SELECT * FROM Steam WHERE steam_appId = %s"
    data = (gameId, )
    cursor.execute(sql, data)
    
    return cursor.fetchall()

def insertGameDetail(gameId, conn):
    if selectGame(conn, gameId) == None:
        gameData = getGameDetailApi(gameId)
        insertStatement(conn, gameData, gameId)
        return selectGame(conn, gameId)
    else:
        return selectGame(conn, gameId)

