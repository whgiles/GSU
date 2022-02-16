from sqlalchemy import Table, Column, MetaData, create_engine, INTEGER, TIMESTAMP, TEXT, ARRAY
from pmaw import PushshiftAPI
from datetime import datetime
import pandas as pd
import time
import logging
import numpy as np
import advertools as adv

# set logger
logger = logging.getLogger('__name__')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('./logs_no_comments.log')
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

# SQL ALCHEMY SETUP ---------------------------------------------------------------------------------------------------
db_string = "postgresql://wsb:wsb@localhost:5432/wsb"

db = create_engine(db_string)
meta = MetaData()

submissions_table = Table('wsb_submissions', meta,
                          Column('index', INTEGER),
                          Column('submission_id', TEXT),
                          Column('title', TEXT),
                          Column('created', TIMESTAMP),
                          Column('author', TEXT),
                          Column('ticker_mentioned', TEXT),
                          Column('subreddit', TEXT),
                          Column('emotes', ARRAY(TEXT)),
                          Column('rocket_emotes', INTEGER)
                          )

comments_table = Table('wsb_comments', meta,
                       Column('index', INTEGER),
                       Column('comment_id', INTEGER),
                       Column('body', TEXT),
                       Column('created', TIMESTAMP),
                       Column('author', TEXT),
                       Column('rocket_emotes', INTEGER),
                       Column('subreddit', TEXT),
                       Column('emotes', ARRAY(TEXT)),
                       Column('submission_key', TEXT)
                       )
conn = db.connect()


# ---------------------------------------------------------------------------------------------------------------------
# USING PUSHSHIFT API TO COLLECT DATA----------------------------------------------------------------------------

def collect_data(after, before, connect, persist=True, comments=True, submissions=True):
    start = time.time()

    api = PushshiftAPI()
    start_at = int(datetime.strptime(after, '%Y-%m-%d %H:%M:%S').timestamp())
    end_at = int(datetime.strptime(before, '%Y-%m-%d %H:%M:%S').timestamp())
    print(start_at, end_at)
    # linked ids contain t3_ before the submission's id

    num_comm = 0
    num_sub = 0
    try:
        if comments:
            comments_from_api = api.search_comments(mem_safe=True, safe_exit=True, before=end_at, after=start_at,
                                                    subreddit='wallstreetbets',
                                                    fields=["id", "created_utc", "body", "author", "link_id",
                                                            "subreddit"])

            print('PERSISTING COMMENTS')
            if persist:
                for comment in comments_from_api:
                    id = comment['id']
                    created = datetime.utcfromtimestamp(comment['created_utc']).strftime('%Y-%m-%d %H:%M:%S')
                    body = comment['body']
                    author = comment['author']
                    submission_key = comment['link_id'].split('_')[1]
                    subreddit = comment['subreddit']

                    connect.execute(
                        comments_table.insert().values(comment_id=id, body=body, created=created, author=author,
                                                       subreddit=subreddit,
                                                       submission_key=submission_key))
                    num_comm += 1

        if submissions:
            submissions_from_api = api.search_submissions(mem_safe=True, safe_exit=True, before=end_at, after=start_at,
                                                          subreddit='wallstreetbets',
                                                          fields=['author', 'id', 'title', 'created_utc', 'subreddit'])

            print('PERSISTING SUBMISSIONS')
            if persist:
                for submission in submissions_from_api:
                    id = submission['id']
                    created = datetime.utcfromtimestamp(submission['created_utc']).strftime('%Y-%m-%d %H:%M:%S')
                    author = submission['author']
                    title = submission['title']
                    subreddit = submission['subreddit']

                    connect.execute(
                        submissions_table.insert().values(submission_id=id, title=title, created=created, author=author,
                                                          subreddit=subreddit))
                    num_sub += 1

        total_time = time.time() - start
        info = {'start_at': after,
                'end_at': before,
                'session time': total_time,
                'num of subs': num_sub,
                'num of comments': num_comm
                }
        logger.info(str(info))

    except Exception as e:
        logging.error(e)
        exit()


# make 9 random hour long time frames for every date between start and end dates
def random_time_frame(start, end):
    dates = pd.date_range(start=start, end=end, freq='d')

    random_dates = []
    for i in range(1, len(dates)):
        hours = pd.date_range(start=dates[i - 1], end=dates[i], freq='1h')
        rand_ints = np.random.randint(0, len(hours) - 2, size=9)
        for rint in rand_ints:
            time_frame = [hours[rint], hours[rint + 1]]
            random_dates.append(time_frame)

    return random_dates


def generate_data_by_dates(start_at, end_at, random=False):
    if random:
        time_frames = random_time_frame(start_at, end_at)
        with db.connect() as conn:
            for idx, val in enumerate(time_frames):
                start_at = str(val[0])
                end_at = str(val[1])

                collect_data(start_at, end_at, conn, persist=True, comments=False, submissions=True)

                print(
                    f'-------------------------------------------{start_at}----------------------------------------------->')
                print(
                    f'------`----------------------------------------------------------------------------------------->')
    else:
        dates = pd.date_range(start=start_at, end=end_at, freq='d')
        with db.connect() as conn:
            for i in range(1, len(dates)):
                start = str(dates[i - 1])
                end = str(dates[i])
                collect_data(start, end, conn, persist=True, comments=False, submissions=True)

                print(
                    f'-------------------------------------------{start}----------------------------------------------->')
                print(
                    f'----------------------------------------------------------------------------------------------->')


if __name__ == '__main__':
    generate_data_by_dates(start_at='3/01/2021', end_at='4/01/2021', random=True)

# def text_analysis(str):
#     return adv.extract_emoji(str)['emoji_flat']
