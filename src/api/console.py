import threading
import time
from repositories import TickerRepository
from stocks_exchange import Stock


def thread_worker():
    tickers = TickerRepository().all()
    stock = Stock()

    for ticker in tickers:
        print('--------------')
        print("Ticker:" + ticker.symbol)
        print("Ticker price: " + str(ticker.local_price))
        new_ticker = stock.updateTickerFromConsole(ticker)
        print("Ticker new price: " + str(new_ticker.local_price))
        print('--------------')


while True:
    ticker_worker = threading.Thread(name='Ticker Thread Worker', target=thread_worker, daemon=True)
    ticker_worker.start()
    time.sleep(15)
