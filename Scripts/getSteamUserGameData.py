import requests
import pandas as pd
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

import aiohttp
import asyncio

async def fetch_friend_games(session, friend_id, api_key):
    url = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={friend_id}&format=json&include_appinfo=true'
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            return None

async def get_friend_games_async(friend_ids, api_key):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_friend_games(session, friend_id, api_key) for friend_id in friend_ids]
        return await asyncio.gather(*tasks)
    