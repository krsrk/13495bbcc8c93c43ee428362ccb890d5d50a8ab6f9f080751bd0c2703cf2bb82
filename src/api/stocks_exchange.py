import urllib.request as request_end_point
import urllib.error as request_error
import json
from datetime import date, time, timedelta
from repositories import TickerRepository
from schemas import TickerResponseModel


class Stock:
    ticker = {}
    has_iex_response_error = False
    error_iex_data = {}

    def processQuote(self, ticker_symbol: str):
        """1.- Check if ticker exists(in DB and IEX)"""
        if self.checkIfTickerExists(ticker_symbol):
            """Checks if ticker can update"""
            if self.checkIfTickerCanUpdate():
                """Query IEX with the new price"""
            else:
                """Return the ticker"""
        elif self.checkIfTickerExistsInIex(ticker_symbol):
            """Create the ticker"""


    def updateTicker(self):
        pass

    def queryIEX(self, ticker_symbol: str):
        try:
            ticker_symbol_lowercase = ticker_symbol.lower()
            iex_endpoint_url = f"https://cloud.iexapis.com/stable/stock/{ticker_symbol_lowercase}/quote?token=pk_0d201a1c16ce46c4bb3b764b22c80fc9"
            request = request_end_point.urlopen(iex_endpoint_url)
            ticker_request_data = json.loads(request.read().decode('utf-8'))
            self.has_iex_response_error = False
            self.ticker = TickerResponseModel(
                symbol=ticker_request_data['symbol'],
                company_name=ticker_request_data['companyName'],
                primary_exchange=ticker_request_data['primaryExchange'],
                local_last_update=ticker_request_data['latestUpdate'],
                local_price=ticker_request_data['iexAskPrice'],
                local_cached=True,
            )
        except request_error.HTTPError as e:
            self.has_iex_response_error = True
            self.ticker = {'error_code': e.code, 'error_message': e.read()}

    def checkIfTickerExists(self, ticker_symbol: str):
        ticker_exists = True

        ticker = TickerRepository().findBySymbol(ticker_symbol)

        if not ticker:
            ticker_exists = False
        else:
            self.ticker = ticker

        return ticker_exists

    def checkIfTickerExistsInIex(self, ticker_symbol:str):
        ticker_exists = True
        query_iex = self.queryIEX(ticker_symbol)
        if self.has_iex_response_error:
            ticker_exists = False
        else:
            self.ticker = query_iex

        return ticker_exists

    def checkIfTickerCanUpdate(self):
        return True
