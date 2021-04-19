from db import Ticker


class TickerRepository:
    repository = Ticker

    def all(self):
        return self.repository.select().get()

    def findBySymbol(self, ticker_symbol: str):
        return self.repository.select().where(self.repository.symbol == ticker_symbol).first()

    def create(self, ticker_data):
        return self.repository.create(
            symbol=ticker_data.symbol,
            company_name=ticker_data.company_name,
            primary_exchange=ticker_data.primary_exchange,
            local_last_update=int(ticker_data.local_last_update),
            local_price=ticker_data.local_price,
            local_cached=ticker_data.local_cached,
        )

    def updateByField(self, ticker: Ticker, ticker_field: str, ticker_new_value):
        setattr(ticker, ticker_field, ticker_new_value)
        ticker.save()

        return ticker


