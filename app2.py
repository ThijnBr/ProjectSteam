import requests
from flask import Flask, redirect, url_for, session, render_template, request
from flask_openid import OpenID
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

import sys
sys.path.append('Scripts')
import getSteamUserFriends as getDetails
import gameSearch
import predictConcurrentPlayers
import getSales
import sortPlayTime

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
        chart_data = predictConcurrentPlayers.getAllChartData()
        popfriends = sortPlayTime.getGameDatabase(sortPlayTime.insertion_sort(sortPlayTime.combineGamePlaytime(steam_id)))
        return render_template('index.html', user_info=user_info, online_friends=online_friends, offline_friends=offline_friends, chart_data=chart_data, popfriends=popfriends)
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/library')
def library():
    return render_template('library.html')

@app.route('/gameinfo')
def gameinfo():
    return render_template('gameinfo.html')

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
