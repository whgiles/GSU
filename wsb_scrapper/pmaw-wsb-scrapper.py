from sqlalchemy import Table, Column, String, MetaData, create_engine, INTEGER, FLOAT, TIMESTAMP, TEXT, ARRAY
from pmaw import PushshiftAPI
from datetime import datetime
import numpy as np
import pandas as pd
import time
import advertools as adv

start = time.time()
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
db.connect()
# ---------------------------------------------------------------------------------------------------------------------
# USING PUSHSHIFT API TO COLLECT DATA----------------------------------------------------------------------------

collect_data = True
if collect_data:

    api = PushshiftAPI()

    start_at = int(datetime.strptime('20210102T1900', '%Y%m%dT%H%M').timestamp())
    end_at = int(datetime.strptime('20210102T1915', '%Y%m%dT%H%M').timestamp())

    # linked ids contain t3_ before the submission's id
    comments_from_api = api.search_comments(mem_safe=True, safe_exit=True, before=end_at, after=start_at,
                                            subreddit='wallstreetbets',
                                            fields=["id", "created_utc", "body", "author", "link_id", "subreddit"])

    submissions_from_api = api.search_submissions(mem_safe=True, safe_exit=True, before=end_at, after=start_at,
                                                  subreddit='wallstreetbets',
                                                  fields=['author', 'id', 'title', 'created_utc', 'subreddit'])


    def text_analysis(str):
        return adv.extract_emoji(str)['emoji_flat']


    with db.connect() as conn:
        for submission in submissions_from_api:
            id = submission['id']
            created = datetime.utcfromtimestamp(submission['created_utc']).strftime('%Y-%m-%d %H:%M:%S')
            author = submission['author']
            title = submission['title']
            subreddit = submission['subreddit']
            emotes = text_analysis(title)

            conn.execute(
                submissions_table.insert().values(submission_id=id, title=title, created=created, author=author,
                                                  subreddit=subreddit, emotes=emotes))

        for comment in comments_from_api:
            id = comment['id']
            created = datetime.utcfromtimestamp(comment['created_utc']).strftime('%Y-%m-%d %H:%M:%S')
            body = comment['body']
            author = comment['author']
            submission_key = comment['link_id'].split('_')[1]
            subreddit = comment['subreddit']
            emotes = text_analysis(body)

            conn.execute(
                comments_table.insert().values(comment_id=id, body=body, created=created, author=author,
                                               subreddit=subreddit,
                                               submission_key=submission_key, emotes=emotes))
end = time.time()
print('Total time: ', end - start)
# ---------------------------------------------------------------------------------------------------------------------
# EXTRACTING FORM DATABASE --------------------------------------------------------------------------------------

# df = pd.read_sql_table('wsb_comments', db)
# print(df)
