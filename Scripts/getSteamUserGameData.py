import requests

apikey = '14B0152189C811A5DE80FE50EB4DA7CC'
steamID = None

apilink = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={apikey}&steamid={steamID}&format=json&include_appinfo=true'