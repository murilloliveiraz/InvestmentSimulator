from flask import Blueprint, jsonify, abort
from data.db_utils import get_db_connection, TABLE_NAME

import yfinance as yf
import sqlite3
from datetime import datetime, timedelta

def fetch_and_update_data(ticker, start_date):
    """
    Checks the database for the latest data for a given ticker,
    fetches new data, and updates the database using a robust method.

    Args:
        ticker (str): The stock ticker symbol.
        start_date (str): The earliest date from which to fetch data (e.g., '2015-01-01').
    """
    print(f"\nProcessing data for: {ticker}")
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT MAX(date) FROM {TABLE_NAME} WHERE ticker = ?", (ticker,))
        latest_date_in_db = cursor.fetchone()[0]
        
        fetch_start_date = start_date
        if latest_date_in_db:
            latest_date_dt = datetime.strptime(latest_date_in_db, '%Y-%m-%d')
            fetch_start_date = (latest_date_dt + timedelta(days=1)).strftime('%Y-%m-%d')
            print(f"Latest data in DB is from {latest_date_in_db}. Fetching new data from {fetch_start_date} to today.")
        else:
            print(f"No data found for {ticker}. Fetching from {start_date} to today.")
            
        data = yf.download(ticker, start=fetch_start_date, end=datetime.now().strftime('%Y-%m-%d'))
        
        if not data.empty:
            data.reset_index(inplace=True)
            data.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
            data['ticker'] = ticker
            
            data['date'] = data['date'].dt.strftime('%Y-%m-%d')

            data = data[['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']]

            rows_to_insert = data.values.tolist()

            sql_insert_command = f'''
                INSERT OR IGNORE INTO {TABLE_NAME} (ticker, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            
            cursor.executemany(sql_insert_command, rows_to_insert)
            conn.commit()
            print(f"Successfully updated database for {ticker} with {len(rows_to_insert)} new rows.")
        else:
            print(f"No new data to fetch for {ticker}.")

    except sqlite3.Error as e:
        print(f"Database error for ticker {ticker}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for ticker {ticker}: {e}")
    finally:
        if conn:
            conn.close()
