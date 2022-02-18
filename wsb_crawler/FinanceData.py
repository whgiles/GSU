from sqlalchemy import Table, Column, MetaData, create_engine, INTEGER, TIMESTAMP, FLOAT, cast, Date
import pandas as pd
import yfinance as yf


class CustomError(Exception):
    pass


class FinanceData:
    meta = MetaData()
    aggregate_table = Table('aggregate_table', meta,
                            Column('index', INTEGER, primary_key=True),
                            Column('day', TIMESTAMP),
                            Column('number_of_submissions_in_day', INTEGER),
                            Column('sum_of_positive_sentiment', FLOAT),
                            Column('sum_of_negative_sentiment', FLOAT),
                            Column('number_of_positive_sentiment', INTEGER),
                            Column('number_of_negative_sentiment', INTEGER),
                            Column('rockets', INTEGER),
                            Column('GDP', FLOAT),

                            Column('GME_submissions_in_day', INTEGER),
                            Column('GME_rockets', INTEGER),
                            Column('GME_sum_of_positive_sentiment', FLOAT),
                            Column('GME_sum_of_negative_sentiment', FLOAT),
                            Column('GME_number_of_positive_sentiment', INTEGER),
                            Column('GME_number_of_negative_sentiment', INTEGER),
                            Column('GME_open', FLOAT),
                            Column('GME_close', FLOAT),
                            Column('GME_market_share', FLOAT),
                            Column('GME_volume', FLOAT),
                            Column('GME_call_volume', FLOAT),
                            Column('GME_put_volume', FLOAT),

                            Column('AMC_submissions_in_day', INTEGER),
                            Column('AMC_rockets', INTEGER),
                            Column('AMC_sum_of_positive_sentiment', FLOAT),
                            Column('AMC_sum_of_negative_sentiment', FLOAT),
                            Column('AMC_number_of_positive_sentiment', INTEGER),
                            Column('AMC_number_of_negative_sentiment', INTEGER),
                            Column('AMC_open', FLOAT),
                            Column('AMC_close', FLOAT),
                            Column('AMC_market_share', FLOAT),
                            Column('AMC_volume', FLOAT),
                            Column('AMC_call_volume', FLOAT),
                            Column('AMC_put_volume', FLOAT),

                            Column('BB_submissions_in_day', INTEGER),
                            Column('BB_rockets', INTEGER),
                            Column('BB_sum_of_positive_sentiment', FLOAT),
                            Column('BB_sum_of_negative_sentiment', FLOAT),
                            Column('BB_number_of_positive_sentiment', INTEGER),
                            Column('BB_number_of_negative_sentiment', INTEGER),
                            Column('BB_open', FLOAT),
                            Column('BB_close', FLOAT),
                            Column('BB_market_share', FLOAT),
                            Column('BB_volume', FLOAT),
                            Column('BB_call_volume', FLOAT),
                            Column('BB_put_volume', FLOAT),

                            Column('TSLA_submissions_in_day', INTEGER),
                            Column('TSLA_rockets', INTEGER),
                            Column('TSLA_sum_of_positive_sentiment', FLOAT),
                            Column('TSLA_sum_of_negative_sentiment', FLOAT),
                            Column('TSLA_number_of_positive_sentiment', INTEGER),
                            Column('TSLA_number_of_negative_sentiment', INTEGER),
                            Column('TSLA_open', FLOAT),
                            Column('TSLA_close', FLOAT),
                            Column('TSLA_market_share', FLOAT),
                            Column('TSLA_volume', FLOAT),
                            Column('TSLA_call_volume', FLOAT),
                            Column('TSLA_put_volume', FLOAT)
                            )

    engine = create_engine("postgresql://wsb:wsb@localhost:5432/wsb")
    meta.create_all(engine)

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.financeData = pd.DataFrame()
        self.tickers = ['gme', 'amc', 'bb', 'tsla']

    def add_ticker(self, *args):
        raise CustomError('This is not supported yet. I wont be able to persist added ticker data')
        self.tickers.extend(list(args))

    def collect_data(self):
        ticker_data = yf.download(self.tickers, self.start, self.end)
        self.financeData = ticker_data
        print(self.financeData)

    def persist_data(self):
        with self.engine.connect() as conn:
            for index, row in self.financeData.iterrows():
                print(index)

                exists = bool(conn.execute(f"SELECT COUNT(*) FROM aggregate_table WHERE day = '{index}'"))
                if exists:
                    conn.execute(
                        self.aggregate_table.update().where(self.aggregate_table.c.day == index).values(
                            GME_open=row['Open']['GME'],
                            GME_close=row['Adj Close']['GME'],
                            GME_volume=row['Volume']['GME'],

                            AMC_open=row['Open']['AMC'],
                            AMC_close=row['Adj Close']['AMC'],
                            AMC_volume=row['Volume']['AMC'],

                            BB_open=row['Open']['BB'],
                            BB_close=row['Adj Close']['BB'],
                            BB_volume=row['Volume']['BB'],

                            TSLA_open=row['Open']['TSLA'],
                            TSLA_close=row['Adj Close']['TSLA'],
                            TSLA_volume=row['Volume']['TSLA']
                        )
                    )
                else:
                    conn.execute(
                        self.aggregate_table.insert().values(
                            day=index,
                            GME_open=row['Open']['GME'],
                            GME_close=row['Adj Close']['GME'],
                            GME_volume=row['Volume']['GME'],

                            AMC_open=row['Open']['AMC'],
                            AMC_close=row['Adj Close']['AMC'],
                            AMC_volume=row['Volume']['AMC'],

                            BB_open=row['Open']['BB'],
                            BB_close=row['Adj Close']['BB'],
                            BB_volume=row['Volume']['BB'],

                            TSLA_open=row['Open']['TSLA'],
                            TSLA_close=row['Adj Close']['TSLA'],
                            TSLA_volume=row['Volume']['TSLA']
                        )
                    )
