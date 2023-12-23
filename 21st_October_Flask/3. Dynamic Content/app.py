from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Welcome to the Home Page!</h1>'

@app.route('/user/<username>')
def show_user(username):
    return f'<b>User Name:</b> {username}'

@app.route('/id/<int:user_id>')
def show_id(user_id):
    return f'<b>User ID:</b> {user_id}'

if __name__ == '__main__':
    app.run(debug=True)
