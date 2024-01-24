import requests
from flask import Flask, redirect, url_for, session, render_template, request
from flask_openid import OpenID
import asyncio

import Scripts.getSteamUserFriends as getDetails
import Scripts.gameSearch
import Scripts.predictConcurrentPlayers
import Scripts.getSales
import Scripts.sortPlayTime
import Scripts.getSteamUserGameData
import Scripts.getGameFromDatabase
import Scripts.getGameFromDatabase

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
        print(online_friends)
        offline_friends = [x for x in friends_details if x['info'] == 'Offline']
        chart_data = predictConcurrentPlayers.getAllChartData(predictConcurrentPlayers.getConcurrentPlayersFromDatabase(True))
        popfriends = sortPlayTime.getGameDatabase(sortPlayTime.insertion_sort(sortPlayTime.combineGamePlaytime(steam_id)))
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
        gameCount = asyncio.run(getSteamUserGameData.fetch_friend_games(steam_id, None))["response"]["games"]
        gameList = []
        for x in gameCount:
            gameId = x['appid']
            gameList.append(getGameFromDatabase.getLibraryGames(gameId))
        
        return render_template('library.html', gameCount=gameCount, gameList=gameList)
    else:
        return redirect(url_for('login'))
    

@app.route('/gameinfo')
def gameinfo():
    steam_id = 271590                        #request.args.get('steam_id', default = 1, type = int)
    games = getGameFromDatabase.getLibraryGames(steam_id)
    return render_template('gameinfo.html', games=games)


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
    app.run(debug=True)
