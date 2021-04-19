from peewee import *


db_engine = MySQLDatabase(
    'stock',
    user='root',
    password='root',
    host='db',
    port=3306
)


class Ticker(Model):
    symbol = CharField(max_length=10, index=True, unique=True)
    company_name = CharField(max_length=256)
    primary_exchange = CharField(max_length=500)
    local_last_update = TimestampField()
    local_price = DecimalField()
    local_cached = BooleanField()

    def __str__(self):
        return self.symbol

    class Meta:
        database = db_engine
        table_name = 'tickers'

