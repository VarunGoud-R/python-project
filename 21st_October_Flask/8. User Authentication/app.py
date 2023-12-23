from flask import Flask, get_flashed_messages, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Example User model
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def check_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return self.password == hashed_password

# Example user database (you should replace this with a database)
users = {
    1: User(1, 'user1', hashlib.sha256('password1'.encode()).hexdigest()),
    2: User(2, 'Varun', hashlib.sha256('passwordn'.encode()).hexdigest())
}

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((user for user in users.values() if user.username == username), None)
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password!', 'error')
        print(get_flashed_messages())
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    print(current_user.username)
    return render_template('dashboard.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
