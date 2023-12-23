from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
from queries import *

app = Flask(__name__)

# SQLite database configuration
DATABASE = 'data.sql'

def connection(func):
    def exec(*q):
        try:
            # with sqlite3.connect(DATABASE) as conn:
            conn = sqlite3.connect(DATABASE)
            print(conn)
            cur = conn.cursor()
            func(cur, q)
            data = cur.fetchall()
            conn.commit()
            conn.close()
            return data
        except Exception as e:
            print(f'ERROR: {e}')
    return exec

@connection
def create_table(cur, query):
    # Create the data table
    cur.execute(query[0])
    print("Table data created")

# def connect():
#     return sqlite3.connect(":memory:")

# conn = sqlite3.connect(DATABASE)
# cursor = conn.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS items ( name TEXT );")

# @app.before_request
# def before_request():
#     g.db = sqlite3.connect(DATABASE)
#     # g.db.execute("CREATE TABLE IF NOT EXISTS email_addresses1 ( email TEXT );")
# @app.teardown_request
# def teardown_request(exception):
#     if hasattr(g, 'db'):
#         g.db.close()

@app.route("/", methods=["GET"])
def index():
    data = fetch_data(fetchData)
    print(data)
    # data = list(map(lambda x: {x[0]: x[1:]}, data))
    data = enumerate(data)
    # print(list(data))
    return render_template("index.html", data=data)
    # data = get_items()

@connection
def fetch_data(cur, query):
    # Get all data from the database
    cur.execute(query[0])
    print("Fetched data successfully")

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    age = request.form["age"]
    data = add_record(insertRecord, name, age)
    print(f"{data[0]} - inserted")
    return redirect(url_for('index'))
    # insert_item(new_item)

@connection
def add_record(cur, *query):
    # Insert the data into the database
    params = query[0][1:]
    print(params)
    cur.execute(query[0][0], params)

@app.route("/edit/<int:id>", methods=["GET", "PUT"])
def edit(id):
    data = fetch_record(fetchRecord, id)
    print(data[0])
    return render_template('edit.html', data=data[0])

@connection
def fetch_record(cur, *query):
    # Get particular record data from the database
    params = query[0][1:]
    print(params)
    cur.execute(query[0][0], params)
    print("Fetched record successfully")

@app.route("/modify/<int:id>", methods=["GET", "PUT"])
def modify(id):
    name = request.args.get("name")
    # name = request.form["name"]
    age = request.args.get("age")
    data = modify_record(updateRecord, name, age, id)
    print(f"{data[0]} - updated")
    return redirect(url_for('index'))

@connection
def modify_record(cur, *query):
    # Update the data in the database
    params = query[0][1:]
    print(params)
    cur.execute(query[0][0], params)

@app.route("/remove/<int:id>", methods=["GET", "DELETE"])
def remove(id):
    data = remove_record(deleteRecord, id)
    print(f"{data[0]} - deleted")
    return redirect(url_for('index'))
    # return redirect("/")
    # delete_item_by_id(item_id)

@connection
def remove_record(cur, *query):
    # Delete the data from the database
    params = query[0][1:]
    print(params)
    cur.execute(query[0][0], params)
    # data = cur.fetchall()
    # return data[0]

# def get_items():
#     # with sqlite3.connect(DATABASE) as connection:
#         cursor = connection.cursor()
#         g.db.execute('SELECT * FROM items')
#         items = g.db.cursor().fetchall()
#         print(items)
#         return items
# def insert_item(name):
#     # with sqlite3.connect(DATABASE) as connection:
#         # cursor = connection.cursor()
#         g.db.execute('INSERT INTO items (name) VALUES (?)', (name,))
#         g.db.commit()
# def delete_item_by_id(item_id):
#     with sqlite3.connect(DATABASE) as connection:
#         cursor = connection.cursor()
#         cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
#         connection.commit()

if __name__ == '__main__':
    create_table(createTable)
    app.run(debug=True)
