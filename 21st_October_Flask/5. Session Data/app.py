from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        age = request.form['age']
        # Store user-specific data in the session
        session['username'] = username
        session['age'] = age
        return redirect(url_for('index'))
    # Display user-specific data if available in the session
    username = session.get('username', '')
    age = session.get('age', '')
    return render_template('index.html', username=username, age=age)

@app.route('/logout')
def logout():
    # Clear the session data on logout
    session.pop('username', None)
    session.pop('age', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
