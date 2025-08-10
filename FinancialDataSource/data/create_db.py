import sqlite3

DB_FILE = 'stock_data.db'
TABLE_NAME = 'historical_data'

def setup_database():
    """
    Creates the SQLite database and the 'historical_data' table
    if they do not already exist.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historical_data (
                ticker TEXT NOT NULL,
                date TEXT NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                PRIMARY KEY (ticker, date)
            )
        ''')

        conn.commit()
        conn.close()
        print(f"Database '{DB_FILE}' and table 'historical_data' are ready.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
