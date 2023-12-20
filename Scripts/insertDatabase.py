import psycopg2

conn = psycopg2.connect(
    host="play.miningminigames.uk.to",
    database="Steam",
    user="postgres",
    password="sTEAM.pROJECT")

def insertStatement(conn, obj):
    for value in obj.values():
        steam_appid = value.get('steam_appid')
        name = value.get('name')
        required_age = value.get('required_age')
        is_free = value.get('is_free')
        detailed_description = value.get('detailed_description')
        supported_languages = value.get('supported_languages')
        header_image = value.get('header_image')
        release_date = value.get('release_date')
        recommendations = value.get('recommendations')
        developer = value.get('developer')
        publisher = value.get('publisher')
        cursor = conn.cursor()
        sql = "INSERT INTO Steam (steam_appid, name, required_age, is_free, detailed_description, supported_languages, header_image, release_date, recommendations, developer, publisher) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,)"
        data = (steam_appid, name, required_age, is_free, detailed_description, supported_languages, header_image, release_date, recommendations, developer, publisher)
        cursor.execute(sql, data)

with open('testData.json', 'r') as f:
    data = json.load(f)

length = len(data)
current = 0

for obj in data:
    for value in obj.values():
        print(value.get('type'))
    current += 1
    percentage = (current / length) * 100
    print(f"Percentage: {percentage}%")