import psycopg2

def connect():
    conn = psycopg2.connect(
        host="Play.miningminigames.uk.to",
        database='Project Steam',
        user="postgres",
        password="sTEAM.pROJECT"
    )
    return conn
