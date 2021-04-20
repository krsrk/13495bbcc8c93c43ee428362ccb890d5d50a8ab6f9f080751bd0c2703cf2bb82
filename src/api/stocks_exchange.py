from datetime import timedelta, datetime
from repositories import TickerRepository
from schemas import TickerResponseModel
from services.api import ApiService, IexApiService


class Stock:
    ticker = {}
    has_iex_response_error = False
    error_iex_data = {}

    def processQuote(self, ticker_symbol: str):
        if self.checkIfTickerExists(ticker_symbol):
            if self.checkIfTickerCanUpdate():
                self.getTickerFromStockService(ticker_symbol, False)
                self.updateTicker()
            else:
                self.ticker = TickerResponseModel(
                    symbol=self.ticker.symbol,
                    company_name=self.ticker.company_name,
                    primary_exchange=self.ticker.primary_exchange,
                    local_last_update=str(self.ticker.local_last_update),
                    local_price=self.ticker.local_price,
                    local_cached=True,
                )
        elif self.checkIfTickerExistsInIex(ticker_symbol):
            self.createTicker(self.ticker)

    def createTicker(self, data):
        new_ticker = TickerRepository().create(data)
        self.ticker = TickerResponseModel(
            symbol=new_ticker.symbol,
            company_name=new_ticker.company_name,
            primary_exchange=new_ticker.primary_exchange,
            local_last_update=str(new_ticker.local_last_update),
            local_price=new_ticker.local_price,
            local_cached=True,
        )

    def updateTicker(self):
        updated_ticker = TickerRepository().update(self.ticker)
        self.ticker = TickerResponseModel(
            symbol=updated_ticker.symbol,
            company_name=updated_ticker.company_name,
            primary_exchange=updated_ticker.primary_exchange,
            local_last_update=str(updated_ticker.local_last_update),
            local_price=updated_ticker.local_price,
            local_cached=True,
        )

    def getTickerFromStockService(self, ticker_symbol: str, set_ticker_from_service=True):
        ticker_symbol_lowercase = ticker_symbol.lower()
        api_service = ApiService(IexApiService()).call_api_service(ticker_symbol_lowercase)

        if not api_service.has_request_error:
            if set_ticker_from_service:
                self.ticker = TickerResponseModel(
                    symbol=api_service.request_data['symbol'],
                    company_name=api_service.request_data['companyName'],
                    primary_exchange=api_service.request_data['primaryExchange'],
                    local_last_update=api_service.request_data['latestUpdate'],
                    local_price=api_service.request_data['latestPrice'],
                    local_cached=True,
                )
            else:
                self.ticker.local_price = api_service.request_data['latestPrice']
        else:
            self.has_iex_response_error = api_service.has_request_error
            self.error_iex_data = api_service.error_request_data

    def checkIfTickerExists(self, ticker_symbol: str):
        ticker_exists = True
        ticker = TickerRepository().findBySymbol(ticker_symbol)

        if not ticker:
            ticker_exists = False
        else:
            self.ticker = ticker

        return ticker_exists

    def checkIfTickerExistsInIex(self, ticker_symbol: str):
        ticker_exists = True
        self.getTickerFromStockService(ticker_symbol)

        if self.has_iex_response_error:
            ticker_exists = False

        return ticker_exists

    def checkIfTickerCanUpdate(self):
        ticker_can_update = False

        request_time = datetime.now()
        request_timestamp = datetime.timestamp(request_time)

        local_last_update_timestamp = datetime.timestamp(self.ticker.local_last_update)
        ticker_last_update = datetime.fromtimestamp(local_last_update_timestamp) + timedelta(seconds=15)
        ticker_last_update_timestamp = datetime.timestamp(ticker_last_update)

        if request_timestamp > ticker_last_update_timestamp:
            ticker_can_update = True

        return ticker_can_update
