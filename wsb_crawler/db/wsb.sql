CREATE TABLE wsb_submissions
(
    index SERIAL PRIMARY KEY,
    submission_id varchar(100),
    title TEXT,
    created TIMESTAMP,
    author TEXT,
    tickers_mentioned TEXT,
    subreddit TEXT,
    emotes TEXT ARRAY
);
CREATE TABLE wsb_comments
(
    index SERIAL PRIMARY KEY,
    comment_id varchar(100),
    body TEXT,
    created TIMESTAMP,
    author TEXT,
    emotes TEXT ARRAY,
    subreddit TEXT,
    submission_key TEXT
);