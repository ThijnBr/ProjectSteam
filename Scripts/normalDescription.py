from bs4 import BeautifulSoup

def getNormalDescription(data):
    desc = BeautifulSoup(data, 'html.parser')
    plainDesc = desc.get_text(separator=' ', strip=True)
    return plainDesc
