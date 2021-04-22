from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import db_engine as conn
from db import Ticker
from stocks_exchange import Stock
from schemas import TickerRequestModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Server Events
@app.on_event('startup')
def startup():
    if conn.is_closed():
        conn.connect()

    conn.create_tables([Ticker])


@app.on_event('shutdown')
def shutdown():
    if not conn.is_closed():
        conn.close()


# Server Routes
@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get('/quote/ticker/{ticker_symbol}')
async def get_quote(ticker_symbol: str):
    stock = Stock()
    stock.processQuote(ticker_symbol)

    if stock.has_iex_response_error:
        raise HTTPException(status_code=stock.error_iex_data['error_code'],
                            detail=stock.error_iex_data['error_message'])

    return stock.ticker


@app.post('/stock/buy/ticker/{ticker_symbol}/{price}')
async def buy_stock(ticker_symbol: str, price: float):
    buy_stock_request = Stock().processBuyTickerStock(ticker_symbol, price)

    if not buy_stock_request['result']:
        raise HTTPException(status_code=buy_stock_request['code'], detail=buy_stock_request)

    return buy_stock_request


@app.post('/stock/buy/ticker/{ticker_symbol}/{price}/{confirmation}')
async def buy_stock_confirmation(ticker_symbol: str, price: float, confirmation: bool):
    return {ticker_symbol, price, confirmation}
