# YFINANCE_Market

YFINANCE Market which provides you service of real time stocks rate ups and down using real stocks analysis

+--------+        +------------+        +------------+
| Client |  -->   | FastAPI App|  -->   | SQLite DB  |
+--------+        +------------+        +------------+
     ↑                  ↑
     |                  |
  TestClient        yfinance (mocked)
