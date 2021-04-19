from fastapi import FastAPI, HTTPException
from db import db_engine as conn
from db import Ticker

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
    pass
