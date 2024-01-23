import requests
import os
import pandas as pd

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

import aiohttp
import asyncio

df = pd.read_csv('..\Api\ApiKeys.csv')
api_key = df.iloc[0, 1]

#makes session and tasks for a list of friends_ids. returns all games from friends async.
async def get_friend_games_async(friend_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_friend_games(friend_id, session) for friend_id in friend_ids]
        return await asyncio.gather(*tasks)
    
#getowned games of a single steam user.
async def fetch_friend_games(friend_id, session):
    url = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={friend_id}&format=json&include_appinfo=true'

    if session is None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
    else:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

    