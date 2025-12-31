CREATE TABLE IF NOT EXISTS stocks(


       ID integer PRIMARY KEY AUTOINCREMENT,
       ticker text,
       date text,
       open REAL,
       high REAL,
       low REAL,
       close REAL,
       volume INT
       
       
    );
