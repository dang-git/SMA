# -*- coding: utf-8 -*-

import tweepy
from tweepy import OAuthHandler
import pandas as pd
import datetime
import time

consumer_key = 'C07glXzPqKPa95qYwiwoJshXI'
consumer_secret = 'k94YFxtT3PYfAxjZO8bznHZd9dPF7QrT38vJLXhpDz5dqM4HJ5'
access_token = '2399374735-Y0Zw6m1CoRbE0hLzGOYUjRIx4eyl3hZ9SML9o8N'
access_secret = 'dC87GLGLU4PLuVsM1ddKONKo9YMxJSXTunibROrXibZ0E'
proxy = 'cache.srv.pointwest.com.ph:3128'

def searchKeyWord(input):
    date_extracted = datetime.datetime.today().strftime("%m-%d-%Y %H:%M:%S")
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, proxy=proxy)
    keys = input.split(',')
    print(input)
    key = '("' + '") OR ("'.join(keys) + '")'
    lapse = 10
    start = time.time()
    run = True
    df = pd.DataFrame()
    rows_list = []
    tweetid = []
    while run:
        try:
            new_tweets = tweepy.Cursor(api.search, q=key, lang='en').items(1000)
            for tweet in new_tweets:
                runtime = time.time() - start
                if tweet.id not in tweetid and runtime < lapse*60:
                    tweetid.append(tweet.id)
                    row = {}
                    row['tweetid'] = str(tweet.id)
                    row['tweet'] = tweet.text
                    row['dateofposting'] = tweet.created_at
                    row['replytotweetid'] = None
                    row['isretweetoftweetid'] = None
                    row['quotedtweetid'] = None
                    if tweet.in_reply_to_status_id is not None:
                        row['type'] = "reply"
                        row['replytotweetid'] = str(tweet.in_reply_to_status_id)
                    elif tweet.is_quote_status == True:
                        try:
                            row['quotedtweetid'] = str(tweet.quoted_status_id)
                        except AttributeError:
                            row['quotedtweetid'] = None
                            row['type'] = 'quote'
                    elif hasattr(tweet, "retweeted_status") == True:
                        row['isretweetoftweetid'] = str(tweet.retweeted_status.id)
                        row['type'] = "retweet"
                    else:
                        row['type'] = "original"
                    row['fvcount'] = tweet.favorite_count
                    row['rtcount'] = tweet.retweet_count
                    row['userid'] = tweet.user.id
                    row['username'] = tweet.user.screen_name
                    row['name'] = tweet.user.name
                    row['profileimage'] = tweet.user.profile_image_url_https
                    row['verified'] = tweet.user.verified
                    row['flcount'] = tweet.user.followers_count
                    row['userlocation'] = tweet.user.location
                    row['userlanguage'] = tweet.user.lang
                    row['source'] = tweet.source
                    row['geo'] = tweet.geo
                    try:
                        row['coordinates'] = tweet.coordinates['coordinates']
                    except TypeError:
                        row['coordinates'] = None
                    row['tweetlocation'] = tweet.place
                    rows_list.append(row)
                else:
                    run = False
        except tweepy.TweepError as e:
            outfile = open("errors.txt", "a")
            outfile.write("\n")
            outfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
            outfile.write(str(e))
            outfile.close()
            run = False
        except KeyboardInterrupt:
            run = False
        df = pd.DataFrame(rows_list)
        df["dateextracted"] = date_extracted
        df["keywords"] = ",".join(input)