from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

data = {}  # Dictionary to store active data and messages
users = {}

@app.route("/")
def index():
    print("Home Page")
    return render_template("index.html")

@socketio.on("join")
def join_room_handler(room_name, user):
    if room_name not in users.keys():
        print(f"Room created: {room_name}")
    join_room(room_name)
    users.setdefault(room_name, {}).update({request.sid: user})
    data.setdefault(room_name, []).append({request.sid: True})
    # usr = data[room_name][-1].replace(request.sid, user)
    print(f"Users: {users}")
    print(f"Data: {data}")
    usr = f"<b>{users[room_name][request.sid]}</b> joined the room!"
    print(usr)
    # messages = get_messages(room_name)
    # emit("past_messages", messages, to=request.sid)
    emit("message", usr, to=room_name)
    # emit("message", f"You joined the {room_name} room!", to=room_name)

@socketio.on("send_message")
def send_message_handler(message, room_name, user):
    # Store message in your chosen storage (e.g., database)
    # store_message(message, room_name)
    print(f"{request.sid}: {message}")
    # data.setdefault(room_name, []).append(f"{request.sid}: {message}")
    data.setdefault(room_name, []).append({user: message})
    print(f"Messages: {data[room_name]}")
    key = list(data[room_name][-1])[0]
    obj = data[room_name][-1]
    msg = f"<b>{key}:</b> {obj[key]}"
    print(f"Actual chat: {msg}")
    emit("message", msg, to=room_name)
    # emit("new_message", message, to=room_name)

@socketio.on("leave")
def disconnect_handler():
    for room_name, messages in data.items():
        # print(list(i.keys() for i in messages if type(i) == dict))
        # print(list(map(lambda i: i.split(':')[0], messages)))
        # user_ids = set().union(*(d.keys() for d in users[room_name]))
        # user_ids = list(k for i in users[room_name] for k in i.keys())
        user_ids = list(k for k in users[room_name])
        print(f"User Ids: {user_ids}")
        if request.sid in user_ids:
            print(f"Removed {request.sid} from {room_name}")
            # messages = [message for message in messages if request.sid not in message]
            # messages.remove(f"{request.sid} joined the room!")
            messages.append({request.sid: False})
            usr = f"<b>{users[room_name][request.sid]}</b> left the room!"
            print(usr)
            del users[room_name][request.sid]
            emit("message", usr, to=room_name)
            leave_room(room_name)
            # break
    print(f"Active Users: {users}")

# @socketio.on("message")
# def send_message(message, room_name):
#     # print('Message from {}: {}'.format(data['username'], data['message']))
#     # emit('message', data, broadcast=True)
#     emit("message", f"{request.sid}: {message}", to=room_name)

if __name__ == "__main__":
    # socketio.run(app, debug=True)
    app.run(debug=True)
