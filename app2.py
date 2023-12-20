import requests
from flask import Flask, redirect, url_for, session, render_template
from flask_openid import OpenID

app = Flask(__name__)
app.secret_key = '3f6F9E3cFb4B6aD7c8E5fA2e4D9cB8aF'  # sessie toke
oid = OpenID(app)

def get_steam_userinfo(steam_id, api_key):
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}"
    response = requests.get(url)
    data = response.json()
    return data['response']['players'][0]  # Returns user info

def get_friends_steam_ids(steam_id, api_key):
    friends_url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steam_id}&relationship=friend"
    response = requests.get(friends_url)
    friend_ids = [friend['steamid'] for friend in response.json()['friendslist']['friends']]
    return friend_ids

def get_friends_details(api_key, steam_ids):
    summaries_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={','.join(steam_ids)}"
    response = requests.get(summaries_url)
    return response.json()['response']['players']

@app.route('/')
def index():
    user_info = session.get('user_info')
    if user_info:
        api_key = '591D0EBE4F58FD3539E9016C628B72E0'  # steam api 
        steam_id = user_info['steamid']
        friend_ids = get_friends_steam_ids(steam_id, api_key)
        friends_details = get_friends_details(api_key, friend_ids)
        online_friends = [f for f in friends_details if f['personastate'] != 0]
        offline_friends = [f for f in friends_details if f['personastate'] == 0]
        return render_template('index.html', user_info=user_info, online_friends=online_friends, offline_friends=offline_friends)
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/auth/steam')
@oid.loginhandler
def auth_steam():
    return oid.try_login("http://steamcommunity.com/openid")

@oid.after_login
def create_or_login(resp):
    steam_id = resp.identity_url.split('/')[-1]
    user_info = get_steam_userinfo(steam_id, '591D0EBE4F58FD3539E9016C628B72E0')  # steam api
    session['user_info'] = user_info
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
