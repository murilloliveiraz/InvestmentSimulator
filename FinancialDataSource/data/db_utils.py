import sqlite3

DB_FILE = 'stock_data.db'
TABLE_NAME = 'historical_data'

def get_db_connection():
    """
    Retorna uma nova conexão com o banco de dados SQLite.
    A row_factory é configurada para que os resultados sejam acessíveis
    como dicionários (por nome de coluna).
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn