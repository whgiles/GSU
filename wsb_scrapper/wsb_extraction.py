import numpy as np
import pandas as pd
import datetime
import requests
import json
import pprint
import logging

logging.basicConfig(filename='logfile.log', level=logging.INFO,
                    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S')

start_at = int(datetime.datetime.strptime('20210101T0115','%Y%m%dT%H%M').timestamp())
end_at = int(datetime.datetime.strptime('20210101T1915','%Y%m%dT%H%M').timestamp())
subreddit = 'wallstreetbets'

reddit_data = []


# before and after must be in datetime instance: '%Y%m%dT%H%M' ex. '20210101T1815'
def get_pushshift_page(after, before, sub):

    r = requests.get(
        f'https://api.pushshift.io/reddit/search/comment/?&after={str(after)}&before={str(before)}'
        f'&subreddit={str(sub)}&metadata=true&fields=id,created_utc,body,author,link_id&size=100&sort=asc')

    assert r.status_code == 200
    page = json.loads(r.text)
    # pprint.pp(page)
    return page


def structure_data(comment):
    global reddit_data

    id = comment['id']
    body = comment['body']
    created_utc = comment['created_utc']
    author = comment['author']
    link_id = comment['link_id']

    row = np.array([id, body, created_utc, author, link_id])
    reddit_data.append(row)


def append_page_and_update_before(page):
    global start_at
    global reddit_data
    metadata = page['metadata']

    if metadata['shards']['failed'] != 0:
        logging.error(str(metadata['shards']['failed']) + 'shards failed')
    if metadata['timed_out'] != 0:
        logging.error('session timed out')

    data = page['data']
    for comment in data:
        structure_data(comment)

    start_at = reddit_data[len(reddit_data) - 1][2]
    # print('firstrow: ', reddit_data[0])
    # print('lastrow: ', reddit_data[len(reddit_data)-1])
    # print(start_at)
    logging.info('new start date:' + str(datetime.datetime.fromtimestamp(float(start_at))))


def get_all_data():
    global start_at, end_at, subreddit
    switch = True
    while switch:
        page = get_pushshift_page(start_at, end_at, subreddit)
        if not page['data']:
            switch = False
        append_page_and_update_before(page)



if __name__ == '__main__':
    get_all_data()
    print(len(reddit_data))

