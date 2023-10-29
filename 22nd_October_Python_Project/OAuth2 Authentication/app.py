from flask import Flask, render_template, redirect, url_for, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

GOOGLE_CLIENT_ID = os.getenv("client_id")
GOOGLE_CLIENT_SECRET = os.getenv("client_secret")

@app.route("/")
def index():
    # Redirect the user to Google to authenticate
    # req = request.host_url
    # print(req)
    redirect_uri = url_for("callback", _external=True)
    auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}&scope=email+profile&response_type=code&redirect_uri={redirect_uri}"
    return redirect(auth_url, code=302)

@app.route("/callback")
def callback():
    # Exchange the authorization code for an access token
    code = request.args.get('code')
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'code': code,
        'scope': 'https://www.googleapis.com/auth/drive.metadata.readonly',
        # 'scope': 'https://www.googleapis.com/auth/userinfo.profile',
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('callback', _external=True)
    }

    print(data.get('redirect_uri'))
    response = requests.post(token_url, data=data)
    response_data = response.json()
    access_token = response_data.get('access_token')

    if access_token:
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()
        print(user_info)
        # Display the user's information
        return render_template('index.html', user_info=user_info)
    else:
        return render_template('error.html')

if __name__ == "__main__":
    app.run()
