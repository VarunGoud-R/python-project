from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    websites = ["https://www.google.com", "https://www.youtube.com", "https://www.microsoft.com"]
    data = []
    for website in websites:
        response = requests.get(website)
        soup = BeautifulSoup(response.content, "html.parser")
        data.append(soup.find("title").text)
    return render_template("data.html", data=data)

if __name__ == "__main__":
    app.run()

# if __name__ == '__main__':
#     app.run(host= "0.0.0.0", port = 5000)
