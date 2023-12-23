from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Store connected clients
connected_clients = set()

@app.route('/')
def index():
    print("Home Page")
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    # Called automatically when the server is started
    connected_clients.add(request.sid)
    print(f"Client {request.sid} connected")
    # print(connected_clients)

@socketio.on('disconnect')
def handle_disconnect():
    # Called automatically when the server is stopped
    connected_clients.remove(request.sid)
    print(f"Client {request.sid} disconnected")

# @app.route('/send_notification')
@socketio.on("send_notification")
def send_notification():
    message = "New update! Check it out."
    print(message)
    print(connected_clients)
    # emit('notification', {'message': message}, room=connected_clients)
    emit('notification', {'message': message}, room=request.sid)
    return True

# @app.route("/trigger_notification")  # Example route
# def trigger_notification():
#     # ... your logic to generate notification data
#     notification_data = {"message": "This is a notification!"}
#     socketio.emit("send_notification", notification_data)
#     return "Notification sent!"

if __name__ == '__main__':
    socketio.run(app, debug=True)
