from flask import Blueprint, jsonify, abort
from data.db_utils import get_db_connection
import sqlite3

b3_blueprint = Blueprint('b3_controller', __name__)

@b3_blueprint.route('/historical-data/<ticker>/<start_date>', methods=['GET'])
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
        # A chamada da função get_db_connection() foi corrigida.
        conn = get_db_connection()
        cursor = conn.cursor()

        sql_query = "SELECT date, open, high, low, close, volume FROM historical_data WHERE ticker = ? ORDER BY date ASC;"
        cursor.execute(sql_query, (ticker,))
        
        rows = cursor.fetchall()
        
        if not rows:
            # Retorna 404 (Not Found) se nenhum dado for encontrado no banco.
            abort(404, description=f"Nenhum dado encontrado para o ticker: {ticker}")

        # Converte as linhas em um formato JSON amigável.
        historical_data = [
            {
                'ticker': ticker,
                'date': row['date'],
                'open': row['open'],
                'high': row['high'],
                'low': row['low'],
                'close': row['close'],
                'volume': row['volume']
            } for row in rows
        ]
            
        # Retorna a lista como uma resposta JSON.
        return jsonify(historical_data)

    except sqlite3.Error as e:
        # Em caso de erro no banco de dados, retorna um erro 500.
        abort(500, description=f"Erro de banco de dados: {e}")
    finally:
        if conn:
            conn.close()
