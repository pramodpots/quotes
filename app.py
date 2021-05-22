from os import replace
from numpy.core.fromnumeric import size
import pandas as pd
import numpy as np
import schedule
from config import create_api
import tweepy
import time
import random
import threading


ht1 = [
    '#books', '#bookstagram', '#book', '#booklover', '#reading', '#bookworm', '#bookstagrammer', '#bookish', '#read', 
    '#booknerd', '#bookaddict', '#bibliophile', '#booksofinstagram', '#instabook', '#bookaholic',
    '#bookshelf', '#booksbooksbooks', '#libros', '#readersofinstagram', '#bookphotography',
    '#booklove',  '#art', '#literature', '#author',
    '#quotestagram', '#quotes', '#quoteoftheday', '#quotestoliveby', '#quote', '#inspirationalquotes', '#love',
    '#motivationalquotes', '#poetry', '#motivation', '#life', '#inspiration', '#quotesdaily', '#loveyourself', 
    '#positivevibes','#happy', '#success', '#quotesaboutlife', '#believe', '#selflove',
    '#happiness', '#thoughts', '#lifequotes'
]

CHAR_MAX = 280
api = create_api()
df = pd.read_csv('QUOTE.csv', delimiter=';')
dash = '―'

def tweet_now(msg):
    try:
        api.update_status(msg[0:CHAR_MAX])
    except Exception as e:
        print(e)

def get_quote(df):
    n = df.shape[0]
    rand_idx = np.random.choice(n, size=1, replace=False)
    row = df.iloc[rand_idx]
    df = df.drop(rand_idx)
    return row

def get_tweet():
    qt = get_quote(df)
    quote = qt.iloc[0]['QUOTE']
    author = qt.iloc[0]['AUTHOR']
    
    tweet = f'{quote}\n- {author}'
    if len(tweet) > CHAR_MAX:
        return ''
    
    return tweet

def get_hashtags():
    ht = random.sample(ht1, 7)
    return '\n' + ' '.join(ht)

def tweet_quote():
    tweet = get_tweet()
    if len(tweet) == 0:
        print('skipping this tweet')
        return ''
    htag = get_hashtags()
    txt = tweet + htag
    tweet_now(txt)
    print(txt)

def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()


schedule.every(2).hours.do(run_threaded, tweet_quote)

while True:
    schedule.run_pending()
    time.sleep(1)

