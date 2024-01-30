import psycopg2

def connect():
    conn = psycopg2.connect(
        host="192.168.1.98",
        database='Project Steam',
        user="postgres",
        password="sTEAM.pROJECT"
    )
    return conn
