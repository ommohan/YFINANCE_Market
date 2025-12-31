import sqlite3


def init_db():
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    
    with open("schema.sql","r") as f:
        schema = f.read()
        cursor.executescript(schema)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor.fetchall())

        conn.commit()     
        conn.close()
init_db()
