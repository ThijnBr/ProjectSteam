import os, sys
import flask
from flask import Flask, request, render_template, redirect

import sys
sys.path.append('Scripts')
import getSteamUserData

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
from pysteamsignin.steamsignin import SteamSignIn

app = Flask(__name__)

steamID = None

#functie die wordt uitgevoerd wanneer er met de ip:8080 wordt verbonden
@app.route('/')
def main():
    #kijken of er al op inloggen is geklikt
	shouldLogin = request.args.get('login')
	if shouldLogin is not None:
		steamLogin = SteamSignIn()
		return steamLogin.RedirectUser(steamLogin.ConstructURL('http://localhost:8080/processlogin'))

	return render_template('login.html')

#functie die login processed
@app.route('/processlogin')
def process():
    global steamID
    returnData = request.values
    print(returnData)

    steamLogin = SteamSignIn()
    steamID = steamLogin.ValidateResults(returnData)

    if steamID is not False:
        return redirect('/home')
    else:
        return 'Failed to log in, bad details?'

@app.route('/home')
def homepage():
    print(steamID)
    friends = getSteamUserData.getFriendsData(steamID)
    return render_template('index.html', friends=friends)

@app.route('/vrienden')
def vriendenpage():
    friends = getSteamUserData.getFriendsData(steamID)
    return render_template('vrienden.html', friends=friends)

@app.route('/activiteit')
def activiteitpage():
    return render_template('activiteit.html')
      
if __name__ == '__main__':
	os.environ['FLASK_ENV'] = 'development'
	app.run(host = 'localhost', port = 8080, debug = False)
