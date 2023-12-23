from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        age = request.form['age']
        return render_template('index.html', username=username, age=age)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
