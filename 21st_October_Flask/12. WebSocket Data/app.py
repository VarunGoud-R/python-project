from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Sample data
data = {'value': 0}

def update_data():
    while True:
        time.sleep(5)
        data['value'] = random.randint(1, 100)
        print(data)
        socketio.emit('update_data', {'value': data['value']}, namespace='/test')

@app.route('/')
def index():
    print("Tracking enabled")
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connected')
    emit('update_data', {'value': data['value']})

if __name__ == '__main__':
    t = threading.Thread(target=update_data)
    t.daemon = True
    t.start()
    socketio.run(app, debug=True)
