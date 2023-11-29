import os, sys
import flask
from flask import Flask, request, render_template_string, render_template

import sys
sys.path.append('Scripts')
import getSteamUserData

print()

# Not ideal, but for the sake of an example
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
from pysteamsignin.steamsignin import SteamSignIn

app = Flask(__name__)

@app.route('/')
def main():
	shouldLogin = request.args.get('login')
	if shouldLogin is not None:
		steamLogin = SteamSignIn()
		# Flask expects an explicit return on the route.
		return steamLogin.RedirectUser(steamLogin.ConstructURL('http://localhost:8080/processlogin'))

	return render_template('index.html')

@app.route('/processlogin')
def process():
    returnData = request.values

    steamLogin = SteamSignIn()
    steamID = steamLogin.ValidateResults(returnData)
    
    friendsonline = getOnline()
    friendsoffline = getOffline()
    
    if steamID is not False:
        return render_template('data.html', friendsonline=friendsonline, friendsoffline=friendsoffline)
    else:
        return 'Failed to log in, bad details?'

def getOnline():
    friends = getSteamUserData.FriendsOnline()
    return friends

def getOffline():
    friends = getSteamUserData.FriendsOffline()
    return friends
      
if __name__ == '__main__':
	os.environ['FLASK_ENV'] = 'development'
	app.run(host = 'localhost', port = 8080, debug = False)
