import databaseConnection
from bs4 import BeautifulSoup

def getNormalDescription(data):
    desc = BeautifulSoup(data[0], 'html.parser')
    plainDesc = desc.get_text(separator=' ', strip=True)
    return plainDesc
