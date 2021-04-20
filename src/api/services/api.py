from __future__ import annotations
from abc import ABC, abstractmethod
import urllib.request as request_end_point
import urllib.error as request_error
import json


class ApiService:
    """
    The Api Service Context
    """

    def __init__(self, api: Api) -> None:
        self._api = api

    @property
    def api(self) -> Api:
        return self._api

    @api.setter
    def api(self, api: Api) -> None:
        self._api = api

    def call_api_service(self, param):
        return self._api.fetch(param)


class Api(ABC):
    """
    The Api Interface
    """

    @abstractmethod
    def fetch(self, ticker_symbol: str):
        pass


class IexApiService(Api):
    has_request_error = False
    error_request_data = {}
    request_data = {}

    def fetch(self, ticker_symbol: str) -> IexApiService:
        try:
            endpoint_url = f"https://cloud.iexapis.com/stable/stock/{ticker_symbol}/quote?token=pk_0d201a1c16ce46c4bb3b764b22c80fc9"
            request = request_end_point.urlopen(endpoint_url)
            self.request_data = json.loads(request.read().decode('utf-8'))
        except request_error.HTTPError as e:
            self.has_request_error = True
            self.error_request_data = {'error_code': e.code, 'error_message': e.read().decode("utf-8")}

        return self
