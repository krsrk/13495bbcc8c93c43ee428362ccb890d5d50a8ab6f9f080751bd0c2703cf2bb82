import datetime

from db import Ticker
from datetime import datetime


class TickerRepository:
    repository = Ticker

    def all(self):
        return self.repository.select()

    def findBySymbol(self, ticker_symbol: str):
        return self.repository.select().where(self.repository.symbol == ticker_symbol).first()

    def create(self, ticker_data):
        last_update_timestamp = datetime.now().timestamp()
        ticker_price = float(ticker_data.local_price)
        ticker_price_with_fee = ticker_price * 0.1

        return self.repository.create(
            symbol=ticker_data.symbol,
            company_name=ticker_data.company_name,
            primary_exchange=ticker_data.primary_exchange,
            local_last_update=int(last_update_timestamp),
            local_price=ticker_price_with_fee,
            local_cached=ticker_data.local_cached,
        )

    def update(self, ticker):
        last_update_timestamp = datetime.now().timestamp()
        ticker_price = ticker.local_price
        ticker_price_with_fee = ticker_price + (ticker_price * 0.1)

        ticker.local_last_update = int(last_update_timestamp)
        ticker.local_price = ticker_price_with_fee
        ticker.save()

        return ticker

    def updateByField(self, ticker: Ticker, ticker_field: str, ticker_new_value):
        setattr(ticker, ticker_field, ticker_new_value)
        ticker.save()

        return ticker
