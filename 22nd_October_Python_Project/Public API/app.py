from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    user = "sudh9931"
    print(user)
    response = requests.get("https://api.github.com/users/" + user)
    data = response.json()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run()
