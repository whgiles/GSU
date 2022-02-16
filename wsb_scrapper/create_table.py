from sqlalchemy import Table, Column, MetaData, create_engine, INTEGER, TIMESTAMP, TEXT, ARRAY, FLOAT

db_string = "postgresql://wsb:wsb@localhost:5432/wsb"

engine = create_engine(db_string)
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

# aggregate_table.create(engine)
# unique_submissions_table.create(engine)
with engine.connect() as conn:
    # saving a copied table in case of error
    # conn.execute('SELECT COUNT(*) FROM copy_table')

    # move wsb_submissions into unique table
    # conn.execute('INSERT INTO unique_wsb_submissions (submission_id, title, created, author) SELECT DISTINCT ON '
    #              '(submission_id) submission_id, title, created, author FROM wsb_submissions')

    # results = conn.execute("SELECT * FROM unique_wsb_submissions WHERE CAST(created AS DATE) = '2021-01-01'")
    results = conn.execute("SELECT * FROM wsb_submissions WHERE index = 1")
    print(results.first().title)
    print(type(results))
