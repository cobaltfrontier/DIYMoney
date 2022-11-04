from app import db, app
from app.db_connect import connect
import yfinance as yf

def get_ticker():
    conn = connect()
    with conn.cursor() as cur:
        sql = f'SELECT ticker_symbol '\
              f'from ticker'
        cur.execute(sql)
        return cur.fetchall()

def get_stock_price(symbol):
    ticker_yahoo = yf.Ticker(symbol)
    data = ticker_yahoo.history()
    last_quote = (data.tail(1)['Close'].iloc[0])
    return last_quote

def update_price(symbol, price):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'UPDATE ticker SET current_price = {price} WHERE ticker_symbol like "{symbol}";'
        try:
            cur.execute(sql)
            conn.commit()
        except:
            print("Didn't work")


def post_ticker_prices():
    tickers = get_ticker()
    for ticker in tickers:
        symbol = ticker['ticker_symbol']
        if symbol == "CASH":
            price = 1
        else:
            price = get_stock_price(ticker['ticker_symbol'])
            print(f"{symbol} {price}")
            update_price(symbol, price)



# call get ticker function and set to a dictionary (function 2)
# for ticker in tickers
# to access a cell in a dictionary you call the row and column
#• Example ticker[‘ticker_id’]
#• # inside the for loop, check if it is a cash ticker, if it is cash, set price to 1.
#• # otherwise, grab the price by sending the symbol to function 3, returning back the
#price.
#• # finally, send the symbol and the new price up to function 4, which updates table.



