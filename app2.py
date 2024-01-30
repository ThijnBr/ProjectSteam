import requests
from flask import Flask, redirect, url_for, session, render_template, request
from flask_openid import OpenID
import asyncio

import os
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

#script imports
import Scripts.getSteamUserFriends as getDetails
import Scripts.gameSearch as gameSearch
import Scripts.predictConcurrentPlayers as predictConcurrentPlayers
import Scripts.getSales as getSales
import Scripts.sortPlayTime as sortPlayTime
import Scripts.getSteamUserGameData as getSteamUserGameData
import Scripts.getGameFromDatabase as getGameFromDatabase

app = Flask(__name__)
app.secret_key = '3f6F9E3cFb4B6aD7c8E5fA2e4D9cB8aF'  # sessie toke
oid = OpenID(app)

@app.route('/')
def index():
    user_info = session.get('user_info')
    if user_info:
        steam_id = user_info['steamid']
        friends_details = getDetails.getFriendsData(steam_id)
        online_friends = [x for x in friends_details if x['info'] != 'Offline']
        offline_friends = [x for x in friends_details if x['info'] == 'Offline']
        chart_data = predictConcurrentPlayers.getAllChartData(predictConcurrentPlayers.getConcurrentPlayersFromDatabase(True, None))
        popfriends = sortPlayTime.getGameDatabase(sortPlayTime.mergeSort(sortPlayTime.combineGamePlaytime(steam_id)))
        return render_template('index.html', user_info=user_info, online_friends=online_friends, offline_friends=offline_friends, chart_data=chart_data, popfriends=popfriends)
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/library')
def library():
    user_info = session.get('user_info')
    if session.get('user_info'):
        steam_id = user_info['steamid']
        friends_details = getDetails.getFriendsData(steam_id)
        online_friends = [x for x in friends_details if x['info'] != 'Offline']
        offline_friends = [x for x in friends_details if x['info'] == 'Offline']
        gameData = asyncio.run(getSteamUserGameData.fetch_friend_games(steam_id, None))["response"]["games"]
        appids = []
        for x in gameData:
            appids.append(x['appid'])
        libraryGames = asyncio.run(getGameFromDatabase.getLibraryGames(appids))
        return render_template('library.html', gameList=libraryGames, gameCount = len(libraryGames), online_friends = online_friends, offline_friends = offline_friends)
    else:
        return redirect(url_for('login'))
    

@app.route('/gameinfo/<game_id>')
def game_info(game_id):
    # Use game_id to fetch data from the database
    game_data = getGameFromDatabase.getDetailedGames(game_id)
    # Pass the fetched data to the gameinfo.html template
    return render_template('gameinfo.html', games=game_data)


@app.route('/auth/steam')
@oid.loginhandler
def auth_steam():
    return oid.try_login("http://steamcommunity.com/openid")

@oid.after_login
def create_or_login(resp):
    steam_id = resp.identity_url.split('/')[-1]
    user_info = getDetails.getUserInfo(steam_id)
    session['user_info'] = user_info
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('search').lower()
    if query == '':
        return html
    results = gameSearch.getGames(query)
    
    html = ''
    for x in results:
        html += f'<img src="{x[0]}">'
    
    return html

@app.route('/sales')
def sales():
    user_info = session.get('user_info')
    if user_info:
        steam_id = user_info['steamid']
        salesData = getSales.getSalesOnWishlist(steam_id)
        popularSales = getSales.getSalesInPopular()
    else:
        return redirect(url_for('login'))
    return render_template('Sales.html', sales=salesData, popular=popularSales)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
