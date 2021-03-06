import json
from datetime import timedelta, datetime
from repositories import TickerRepository
from schemas import TickerResponseModel
from services.api import ApiService, IexApiService


class Stock:
    TIME_IN_SEC_TO_QUERY_IEX = 15

    ticker = {}
    has_iex_response_error = False
    error_iex_data = {}

    def processQuote(self, ticker_symbol: str):
        if self.checkIfTickerExists(ticker_symbol):
            if self.checkIfTickerCanUpdate():
                self.getTickerFromStockService(ticker_symbol, False)
                self.updateTicker()
            else:
                TickerRepository().updateByField(self.ticker, 'local_cached', True)
                self.ticker = TickerResponseModel(
                    symbol=self.ticker.symbol,
                    company_name=self.ticker.company_name,
                    primary_exchange=self.ticker.primary_exchange,
                    local_last_update=str(self.ticker.local_last_update),
                    local_price=self.ticker.local_price,
                    local_cached=self.ticker.local_cached,
                )
        elif self.checkIfTickerExistsInIex(ticker_symbol):
            self.createTicker(self.ticker)

    def processBuyTickerStock(self, ticker_symbol: str, price: float):
        buy_stock_result = {'code': 200, 'result': True, 'message': 'Successful Transaction!!', 'ticker': {}}

        if self.checkIfTickerExists(ticker_symbol):
            if self.checkIfPriceHasChanged(ticker_symbol, price):
                self.updateTicker()
                buy_stock_result['code'] = 422
                buy_stock_result['result'] = False
                buy_stock_result[
                    'message'] = 'Can not complete transaction the ticker price has changed. Need authorization.'
                buy_stock_result['ticker'] = json.dumps(self.ticker, default=lambda o: o.__dict__, sort_keys=True,
                                                        indent=4)
        else:
            buy_stock_result['code'] = 404
            buy_stock_result['result'] = False
            buy_stock_result['message'] = 'Ticker not found!'

        return buy_stock_result

    def updateTickerFromConsole(self, ticker):
        self.getTickerFromStockService(ticker.symbol)
        ticker.local_price = self.ticker.local_price
        updated_ticker = TickerRepository().update(ticker)

        return TickerResponseModel(
            symbol=updated_ticker.symbol,
            company_name=updated_ticker.company_name,
            primary_exchange=updated_ticker.primary_exchange,
            local_last_update=str(updated_ticker.local_last_update),
            local_price=updated_ticker.local_price,
            local_cached=updated_ticker.local_cached,
        )

    def createTicker(self, data):
        new_ticker = TickerRepository().create(data)
        self.ticker = TickerResponseModel(
            symbol=new_ticker.symbol,
            company_name=new_ticker.company_name,
            primary_exchange=new_ticker.primary_exchange,
            local_last_update=str(new_ticker.local_last_update),
            local_price=new_ticker.local_price,
            local_cached=new_ticker.local_cached,
        )

    def updateTicker(self):
        updated_ticker = TickerRepository().update(self.ticker)
        self.ticker = TickerResponseModel(
            symbol=updated_ticker.symbol,
            company_name=updated_ticker.company_name,
            primary_exchange=updated_ticker.primary_exchange,
            local_last_update=str(updated_ticker.local_last_update),
            local_price=updated_ticker.local_price,
            local_cached=updated_ticker.local_cached,
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
                    local_cached=False,
                )
            else:
                self.ticker.local_price = api_service.request_data['latestPrice']
                self.ticker.local_cached = False
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
        ticker_last_update = datetime.fromtimestamp(local_last_update_timestamp) + timedelta(seconds=self.TIME_IN_SEC_TO_QUERY_IEX)
        ticker_last_update_timestamp = datetime.timestamp(ticker_last_update)

        if request_timestamp > ticker_last_update_timestamp:
            ticker_can_update = True

        return ticker_can_update

    def checkIfPriceHasChanged(self, ticker_symbol: str, price: float):
        price_has_changed = False
        self.getTickerFromStockService(ticker_symbol, False)

        if price != self.ticker.local_price:
            price_has_changed = True

        return price_has_changed
