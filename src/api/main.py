from fastapi import FastAPI, HTTPException
from db import db_engine as conn
from db import Ticker
from stocks_exchange import Stock

app = FastAPI()


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


@app.post('/quote')
async def get_quote(ticker_symbol: str):
    stock = Stock()
    stock.processQuote(ticker_symbol)

    if stock.has_iex_response_error:
        raise HTTPException(status_code=stock.error_iex_data['error_code'],
                             detail=stock.error_iex_data['error_message'])

    return stock.ticker
