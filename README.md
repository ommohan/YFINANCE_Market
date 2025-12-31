# YFINANCE_Market
YFINANCE Market provides real-time stock service rate tracking and by using actual stock data for analysis 
It uses FastAPI for serving endpoints, SQLite for local storage, and mocks yfinance for offline-safe testing.



# Clone the repo
git clone https://github.com/ommohan/YFINANCE_Market.git
cd YFINANCE_Market

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

## 📖 API Documentation

FastAPI provides interactive API docs automatically:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Use these to explore and test endpoints directly in the browser.

## 🗂️ Project Structure
[!Project Strcuture](ProjectStructure.png)

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

![Architecture Diagram](ArchitectureDiagram.png)

__Explanation of Decision and trade offs__
# FAST API:- 
Fast API for backend UI which provide visualize content to user provide lightweight service to TestClient with efficient and in simple manner.

# SQLITE DataBase:-
Lighetweight for file handling using this module which provides connection for our real time stock analysis not concurrent for large deployments

# Mock External Calls:- 
Allow user to avoid from internet connection beneficial for safer browsing and reproducibility.

# Unittest and Pytest:- 
Uses for simplicity and compaitible build in tool which provide python while pytest primarily giving flexiblity and unittest prvides minimal setup behaviour.

# No Pagination and Filtering:-
It Becomes may efficient for lage sacle businesses as because data grows,but it is acceptable for small prototype model

****Assumptions And Instructions****

**1)Hourly data is sufficient for analysis:-**  
The app uses interval="1h" and period="1d" — suitable for demo purposes but not for high-frequency trading or long-term analysis.

**2)No duplicate protection:-**  
If /fetch is called multiple times for the same ticker and date, duplicate rows may be inserted. No deduplication logic is implemented.

**3)No authentication or access control:-**  
All endpoints are public. This is fine for local use but insecure for production.

**4)No retry or caching for API calls :-** 
If yfinance fails due to rate limits or network issues, the app returns an error. No fallback or retry mechanism is in place.

## Extension Q & A:-
 
**How would this scale to handle 10 tickers concurrently?**
Use asyncio.gather() or FastAPI in as a background tasks to fetch multiple tickers in parallel.For heavy workloads like **Celery** and **Redis** which manages concurrently safely

**How would you avoid API rate limits?**
Implenent cahce for current resulting and switches or rotate diffrent api keys against rate loss also if required then use safe proxy pool

**What’s the first architectural change you'd make for production?**
Replace SQLite with PostgreSQL for better concurrency and scalability,flexiblity. Add structured logging, error monitoring (e.g., Sentry), and deploy with Docker with Gunicorn or uvicorn for reverse proxy

**What’s a trading-related pitfall of using this setup as-is?**
The system lacks real-time guarantees — hourly data may be outdated for live trading. There's no validation, alerting, or protection against or missing data, which could lead to poor trading decisions.
