investment_tickers = [
    'PETR4.SA',   # Petrobras
    'VALE3.SA',   # Vale
    'ITUB4.SA',   # Itaú Unibanco
    'BBDC4.SA',   # Bradesco
    '^BVSP'       # Bovespa Index
]

def get_tickers_list():
    print("\nInvestment Tickers List:")
    for ticker in investment_tickers:
        print(f"- {ticker}")