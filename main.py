import unittest
import yfinance as yf
import os 
from fastapi import FastAPI
import sqlite3, pandas as pd
from unittest.mock import patch
from fastapi.testclient import TestClient



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR,"stocks.db")

PERIOD = "1d"
INTERVAL = "1h"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"



app = FastAPI()

@app.get("/")
def root():
    
    return{"message": "Server is runnning:"}

@app.get('/last')
def get_last():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * from stocks ORDER BY date DESC",conn)
    return df.to_dict(orient='records')


@app.get("/history")
def get_history():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * from stocks",conn)
    return df.to_dict(orient='records')

@app.post("/fetch")
def fetch_data(ticker: str):
    data = yf.download(ticker, period=PERIOD ,interval=INTERVAL)
    print(data.head())
    
    if data.empty:
        return {"status":'error',  "message":"NO data Returned"}
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        for index, row in data.iterrows():
            cursor.execute("""
            INSERT INTO stocks (ticker,date,open,high,low,close,volume)
            VALUES(?,?,?,?,?,?,?) 
            """, (ticker, index.strftime(DATE_FORMAT),row['Open'],row['High'],row['Low'],row['Close'],row["Volume"]))
        conn.commit()
        conn.close()
        return {"status": "success", "rows": len(data)}
    except Exception as e:
        return {"status":"error", "rows": str(e)}
    

client = TestClient(app)

class TestFetchEndpoint(unittest.TestCase):
    @patch("app.main.yf.download")   
    def test_fetch_valid_ticker(self, mock_download):
        mock_data = pd.DataFrame({
            "Open": [250.0],
            "High": [255.0],
            "Low": [248.0],
            "Close": [252.0],
            "Volume": [233.0]
        }, index=pd.date_range("2025-12-29", periods=2))

        mock_download.return_value = mock_data

        response = client.post("/fetch", params={"ticker": "TSLA"})
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["rows"], 2)
