import sqlite3
import os
import unittest
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "stocks.db")

class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL, 
            volume INT
        )
        """)
        conn.commit()
        conn.close()

    def test_insert_and_read(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO stocks (ticker, date, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("TSLA", "2025-12-29", 250.0, 255.0, 248.0, 252.0, 100000))
        conn.commit()
        print("Inserted TSLA row")

       
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query("SELECT * FROM stocks", conn)
            print(df)
            print("Rows in DB:", cursor.execute("SELECT COUNT(*) FROM stocks").fetchone())


        conn.close()



        self.assertFalse(df.empty)
        self.assertEqual(len(df),1)
        self.assertEqual(df.iloc[0]["ticker"], "TSLA")
        self.assertEqual(df.iloc[0]["close"], 252.0)


        print("DataFrame contents:\n", df)
        print("Length of DataFrame:", len(df)) 
        print("Columns:", df.columns.tolist())

    def tearDown(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
   

if __name__ == "__main__":
    unittest.main()
