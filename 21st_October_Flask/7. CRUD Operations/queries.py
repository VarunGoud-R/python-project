createTable = """
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER
    )"""

fetchData = "SELECT * FROM data"

fetchRecord = """SELECT * FROM data
    WHERE id = ?"""

insertRecord = """
    INSERT INTO data (
        name, age
    ) VALUES (
        ?, ?
    ) RETURNING *"""

updateRecord = """UPDATE data
    SET name = ?, age = ?
    WHERE id = ?
    RETURNING *"""

deleteRecord = """DELETE FROM data 
    WHERE id = ?
    RETURNING *"""
