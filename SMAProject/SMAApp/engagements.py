# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime


"""::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
FOR DIAGNOSTICS TAB DATA
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"""

def return_engagements(df):
    # tweet count, user count, engagements
    rts = int(df[df["type"] != "retweet"]['rtcount'].sum())
    fvs = int(df['fvcount'].sum())
    desc_js = {"tweets": len(df), "users": df.username.nunique(),
        "engagements": rts+fvs}
    dfu = df.groupby(["username"], sort=False)["flcount"].max().reset_index()
    rh = dfu['flcount'].sum() + dfu.username.nunique()
    desc_js['reach'] = int(rh)
    return desc_js

def return_timeline(df):
    # timeline
    tl = pd.DataFrame(df.dateofposting)
    tl['datehour'] = [i.replace(microsecond=0,second=0) for i in tl.dateofposting]
    tl = tl.groupby(['datehour'], as_index=False).count().reset_index()
    del tl['index']
    tl["int"] = [1000*(t.replace(tzinfo=None)-datetime(1970,1,1)).total_seconds() for t in tl.datehour]
    tl.to_csv("tl.csv")
    chartdata = {'x': tl["int"],
        'name': 'Volume', 'y1': tl['dateofposting'], 'kwargs1': { 'color': '#ef6c00' }
    }
    return chartdata

def return_composition(df):
    data = dict(df.type.value_counts())
    return data

def return_source(df):
    src = dict(df.source.value_counts())
    src_ = {}
    src_["Web Client"]  = src["Twitter Web Client"]
    src_["Android"]  = src["Twitter for Android"]
    src_["iPhone"]  = src["Twitter for iPhone"]
    src_["Others"]  = sum(src.values()) - src_["Web Client"] - src_["Android"] - src_["iPhone"]
    return src_

def return_geocode(df):
    data = {}
    for i in df.coordinates:
        if i != None:
            data[len(data)] = {"lat": i[0], "long": i[1]}
    return data



"""::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
FOR INFLUENCERS TAB DATA
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"""

# set value for filter_ to engagements and flcount only
def return_influencers(df, filter_):
    cols = ["username", "rtcount", "fvcount", "type", "profileimage", "flcount"]
    df = df[cols].reset_index()
    del df['index']
    df = df[df['type'] != 'retweet']
    postcount = df.groupby(['username']).count().reset_index()[['username', 'profileimage']]
    postcount.columns = ['username', 'postcount']
    df = df.groupby(['username', 'flcount', 'profileimage'], sort=False)['rtcount', 'fvcount'].sum().reset_index()
    df = pd.merge(df, postcount, how='left', on=['username'])
    df['engagements'] = df['rtcount'] + df['fvcount']
    df = df.sort_values(filter_, ascending=False).head(10).reset_index()
    data = {"1st": {"username": "@%s" % df['username'][0], "profileimage": df['profileimage'][0], "post": df['postcount'][0], "favorites": df['fvcount'][0], "retweets": df['rtcount'][0], "followers": df['flcount'][0]},
               "2nd": {"username": "@%s" % df['username'][1], "profileimage": df['profileimage'][1], "post": df['postcount'][1], "favorites": df['fvcount'][1], "retweets": df['rtcount'][1], "followers": df['flcount'][1]},
               "3rd": {"username": "@%s" % df['username'][2], "profileimage": df['profileimage'][2], "post": df['postcount'][2], "favorites": df['fvcount'][2], "retweets": df['rtcount'][2], "followers": df['flcount'][2]},
               "4th": {"username": "@%s" % df['username'][3], "profileimage": df['profileimage'][3], "post": df['postcount'][3], "favorites": df['fvcount'][3], "retweets": df['rtcount'][3], "followers": df['flcount'][3]},
               "5th": {"username": "@%s" % df['username'][4], "profileimage": df['profileimage'][4], "post": df['postcount'][4], "favorites": df['fvcount'][4], "retweets": df['rtcount'][4], "followers": df['flcount'][4]}}
    return data



"""::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
FOR INFLUENTIAL POSTS TAB DATA
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"""

def return_infl_posts(df):
    cols = ["username", "profileimage", "flcount", "tweet", "rtcount", "fvcount", "type"]
    df = df[cols].reset_index()
    del df['index']
    df = df[df['type'] != 'retweet']
    df = df.groupby(['username', 'profileimage', 'tweet'], sort=False)['rtcount', 'fvcount', 'flcount'].max().reset_index()
    df = df.sort_values('rtcount', ascending=False).head(10).reset_index()