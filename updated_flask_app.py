
import os, sys
import flask
from flask import Flask, request, render_template, redirect

import sys
sys.path.append('Scripts')
import getSteamUserFriends as getFriends

from pysteamsignin.steamsignin import SteamSignIn

app = Flask(__name__)

steamID = None

# Function that is executed when connecting to ip:8080
@app.route('/')
def main():
    # Checking if the login button has been clicked
    shouldLogin = request.args.get('login')
    if shouldLogin is not None:
        steamLogin = SteamSignIn()
        return steamLogin.RedirectUser(steamLogin.ConstructURL('http://localhost:8080/processlogin'))

    return render_template('index.html')

# Function that processes login
@app.route('/processlogin')
def process():
    global steamID
    returnData = request.values

    steamLogin = SteamSignIn()
    steamID = steamLogin.ValidateResults(returnData)

    if steamID is not False:
        return redirect('/home')
    else:
        return 'Failed to log in, bad details?'

@app.route('/home')
def homepage():
    if steamID:
        friends = getFriends.getFriendsData(steamID)
        return render_template('index.html', friends=friends)
    else:
        return redirect('/')

@app.route('/friends')
def vriendenpage():
    if steamID:
        friends = getFriends.getFriendsData(steamID)
        return render_template('friends.html', friends=friends)
    else:
        return redirect('/')

@app.route('/games')
def activiteitpage():
    return render_template('games.html')
      
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/aa')
def extrapage():
    return render_template('aa.html')

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(host = 'localhost', port = 8080, debug = False)
