from typing import Optional
from pydantic import BaseModel


class TickerRequestModel(BaseModel):
    symbol: str
    company_name: str
    primary_exchange: str
    local_last_update: Optional[str] = None
    local_price: float
    local_cached: bool


class TickerResponseModel(TickerRequestModel):
    symbol: str

