from sqlalchemy import Table, Column, MetaData, create_engine, INTEGER, TIMESTAMP, FLOAT
from nltk.sentiment import vader
import numpy as np
import advertools as adv
import pandas as pd

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


# todo: create the sentiment statistic
def vader_analysis(str):
    sid = vader.SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(str)
    return ss['compound']


def rocket_count(str):
    emotes = adv.extract_emoji(str)['emoji_flat']
    return len([x for x in emotes if x == '🚀'])


class CustomError(Exception):
    pass


# Dates must be in the format yyyy-mm-dd
class FormatData:

    def __init__(self, raw_table_name, db_path, dates):
        self.raw_table_name = raw_table_name
        self.dates = dates
        self.engine = create_engine(db_path)
        self.raw_copy_table = str()
        # todo refactor self.stocks as a dictionary and have a method to add new key words
        self.stocks = [['gme', 'gamestop'],
                       ['bb', 'blackberry'],
                       ['amc'],
                       ['tsla', 'tesla']]
        self.tickers = [x[0] for x in self.stocks]

    # makes a copy of the raw data table (of unique values) that is used throughout this object
    def copy_raw_table(self):
        # todo cashe table name
        with self.engine.connect() as conn:
            copy_name = self.raw_table_name + str(np.random.randint(1000, 2000))
            try:
                sql = f"CREATE TABLE {copy_name} LIKE {self.raw_table_name}; INSERT INTO {copy_name} SELECT * FROM {self.raw_copy_table}"
                conn.execute(sql)
                self.raw_copy_table = copy_name
            except Exception as e:
                raise e

    # sorts observation by ticker(s), then summarizes the sentiment and the amount of rocket emotes
    def summarize_single_observation(self, obs):
        # initializing the summary table
        observation_summary = {}
        for i in self.tickers:
            observation_summary[i] = {
                'rockets': int(),
                'sum_of_positive_sentiment': float(),
                'sum_of_negative_sentiment': float(),
                'number_of_positive_sentiment': int(),
                'number_of_negative_sentiment': int()
            }
        # meta carries information about the observations regardless of ticker
        observation_summary['meta'] = {
            'rockets': int(),
            'sum_of_positive_sentiment': float(),
            'sum_of_negative_sentiment': float(),
            'number_of_positive_sentiment': int(),
            'number_of_negative_sentiment': int()
        }

        sentiment = vader_analysis(obs.title)
        rockets = rocket_count(obs.title) # todo: get number of rocket emotes in text

        for stocks in self.stocks:
            lower_case_obs = obs.lower()
            if any(x in lower_case_obs for x in stocks):
                observation_summary[stocks[0]]['sentiment'] = sentiment
                observation_summary[stocks[0]]['rockets'] = rockets

        return observation_summary

    # Selects observations from the raw_table.copy, and returns its aggregated values
    def aggregate_data_for_single_date(self, date):
        with self.engine as conn:
            sql = f"SELECT * FROM {self.raw_copy_table} WHERE CAST(created AS DATE) = {date}"
            results = conn.execute(sql)

            if len(list(results)) == 0:
                return False

            # initializing dictionary to contain a running summer of daily sentiment and rocket emotes for
            running_summary = {}
            for i in self.tickers:
                running_summary[i] = {
                    'rockets': int(),
                    'sum_of_positive_sentiment': int(),
                    'sum_of_negative_sentiment': int(),
                    'number_of_positive_sentiment': int(),
                    'number_of_negative_sentiment': int(),
                    'number_submissions_in_day': int()
                }
            running_summary['meta'] = {
                'rockets': int(),
                'sum_of_positive_sentiment': int(),
                'sum_of_negative_sentiment': int(),
                'number_of_positive_sentiment': int(),
                'number_of_negative_sentiment': int(),
                'number_of_submissions_in_day': int()
            }
            # iterate through observations and store data in running dictionary
            for obs in date:
                observation_summary = self.summarize_single_observation(obs)
                for i in self.tickers:
                    running_summary[i]['rockets'] += observation_summary[i]['rockets']
                    running_summary[i]['sum_of_positive_sentiment'] += observation_summary[i][
                        'sum_of_positive_sentiment']
                    running_summary[i]['sum_of_negative_sentiment'] += observation_summary[i][
                        'sum_of_negative_sentiment']
                    running_summary[i]['number_of_positive_sentiment'] += observation_summary[i][
                        'number_of_positive_sentiment']
                    running_summary[i]['number_of_negative_sentiment'] += observation_summary[i][
                        'number_of_negative_sentiment']
                    running_summary[i]['number_of_submissions_in_day'] += observation_summary[i][
                        'number_of_submissions_in_day']

                running_summary['meta']['sum_of_positive_sentiment'] += observation_summary['meta'][
                    'sum_of_positive_sentiment']
                running_summary['meta']['sum_of_negative_sentiment'] += observation_summary['meta'][
                    'sum_of_negative_sentiment']
                running_summary['meta']['number_of_positive_sentiment'] += observation_summary['meta'][
                    'number_of_positive_sentiment']
                running_summary['meta']['number_of_negative_sentiment'] += observation_summary['meta'][
                    'number_of_negative_sentiment']
                running_summary['meta']['number_of_submissions_in_day'] += observation_summary['meta'][
                    'number_of_submissions_in_day']
                running_summary['meta']['rockets'] += observation_summary['meta']['rockets']

            return running_summary

    # persist aggregate data to database
    def aggregate_data(self):
        if not bool(self.raw_copy_table):
            raise CustomError("copied table not found. Please call copy_raw_table() before aggregating data")

        with self.engine as conn:
            for date in self.dates:
                daily_summary = self.aggregate_data_for_single_date(date)
                if not daily_summary:
                    continue

                conn.execute(
                    aggregate_table.insert().values(
                        day=date,
                        number_of_submissions_in_day=daily_summary['meta']['number_of_submissions_in_day'],
                        sum_of_positive_sentiment=daily_summary['meta']['sum_of_positive_sentiment'],
                        sum_of_negative_sentiment=daily_summary['meta']['number_of_negative_sentiment'],
                        number_of_positive_sentiment=daily_summary['meta']['number_of_positive_sentiment'],
                        number_of_negative_sentiment=daily_summary['meta']['number_of_negative_sentiment'],
                        rockets=daily_summary['meta']['rockets'],

                        GME_submissions_in_day=daily_summary['gme']['number_of_submissions_in_day'],
                        GME_rockets=daily_summary['gme']['rockets'],
                        GME_sum_of_positive_sentiment=daily_summary['gme']['sum_of_positive_sentiment'],
                        GME_sum_of_negative_sentiment=daily_summary['gme']['sum_of_negative_sentiment'],
                        GME_number_of_positive_sentiment=daily_summary['gme']['number_of_positive_sentiment'],
                        GME_number_of_negative_sentiment=daily_summary['gme']['number_of_negative_sentiment'],

                        AMC_submissions_in_day=daily_summary['amc']['nmber_of_submissions_in_day'],
                        AMC_rockets=daily_summary['amc']['rockets'],
                        AMC_sum_of_positive_sentiment=daily_summary['amc']['sum_of_positive_sentiment'],
                        AMC_sum_of_negative_sentiment=daily_summary['amc']['sum_of_negative_sentiment'],
                        AMC_number_of_positive_sentiment=daily_summary['amc']['number_of_positive_sentiment'],
                        AMC_number_of_negative_sentiment=daily_summary['amc']['number_of_negative_sentiment'],

                        BB_submissions_in_day=daily_summary['bb']['number_of_submissions_in_day'],
                        BB_rockets=daily_summary['bb']['rockets'],
                        BB_sum_of_positive_sentiment=daily_summary['bb']['sum_of_positive_sentiment'],
                        BB_sum_of_negative_sentiment=daily_summary['bb']['sum_of_negative_sentiment'],
                        BB_number_of_positive_sentiment=daily_summary['bb']['number_of_positive_sentiment'],
                        BB_number_of_negative_sentiment=daily_summary['bb']['number_of_negative_sentiment'],

                        TSLA_submissions_in_day=daily_summary['tsla']['number_of_submissions_in_day'],
                        TSLA_rockets=daily_summary['tsla']['rockets'],
                        TSLA_sum_of_positive_sentiment=daily_summary['tsla']['sum_of_positive_sentiment'],
                        TSLA_sum_of_negative_sentiment=daily_summary['tsla']['sum_of_negative_sentiment'],
                        TSLA_number_of_positive_sentiment=daily_summary['tsla']['number_of_positive_sentiment'],
                        TSLA_number_of_negative_sentiment=daily_summary['tsla']['number_of_negative_sentiment']

                    ))
