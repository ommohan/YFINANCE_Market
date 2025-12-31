# YFINANCE_Market
YFINANCE Market provides real-time stock service rate tracking and by using actual stock data for analysis 
It uses FastAPI for serving endpoints, SQLite for local storage, and mocks yfinance for offline-safe testing.



# Clone the repo
git clone https://github.com/yourusername/YFINANCE_Market.git
cd YFINANCE_Market

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py             # or use: uvicorn app.main:app --reload

# Run tests
python -m unittest app/main.py

# Root endpoint — check if server is running
GET http://127.0.0.1:8000/
Response: {"message": "Server is running:"}

# Fetch stock data for a ticker and insert into DB
POST http://127.0.0.1:8000/fetch?ticker=TSLA
Response: {"status": "success", "rows": 1}

# Get all stored stock history
GET http://127.0.0.1:8000/history
Response: [
  {"ID": 1, "ticker": "TSLA", "date": "2025-12-29 00:00:00", "open": 250.0, "high": 255.0, "low": 248.0, "close": 252.0, "volume": 233.0}
]

# Get the most recent entry
GET http://127.0.0.1:8000/last
Response: [
  {"ID": 1, "ticker": "TSLA", "date": "2025-12-29 00:00:00", "open": 250.0, "high": 255.0, "low": 248.0, "close": 252.0, "volume": 233.0}
]
# Run Unit Test (for offline-safe with mocked yfinance)
python -m unittest main.py






## Architecture Diagram

![Architecture Diagram](docs/architecture.png)

+--------+     +-------------+     +-------------+
| Client | --> | FastAPI App | --> | SQLite DB   |
+--------+     +-------------+     +-------------+
    ↑               ↑
    |               |
TestClient   yfinance (mocked)
