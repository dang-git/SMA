# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime


"""::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
DIAGNOSTICS TAB DATA
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

def return_influencers(df):
    cols = ["username", "tweet", "rtcount", "fvcount", "type"]
    df = df[cols].reset_index()
    del df['index']
    df = df[df['type'] != 'retweet']
    print(df.head())
    df = df.groupby(['username', 'tweet'], sort=False)['rtcount', 'fvcount'].max().reset_index()
    df = df.sort_values('rtcount', ascending=False).head(10).reset_index()
    del df['index']
    data = {"1st": {"username": "@%s" % df['username'][0], "favorites": df['fvcount'][0], "retweets": df['rtcount'][0], "tweet": df["tweet"][0]},
               "2nd": {"username": "@%s" % df['username'][1], "favorites": df['fvcount'][1], "retweets": df['rtcount'][1], "tweet": df["tweet"][1]},
               "3rd": {"username": "@%s" % df['username'][2], "favorites": df['fvcount'][2], "retweets": df['rtcount'][2], "tweet": df["tweet"][2]},
               "4th": {"username": "@%s" % df['username'][3], "favorites": df['fvcount'][3], "retweets": df['rtcount'][3], "tweet": df["tweet"][3]},
               "5th": {"username": "@%s" % df['username'][4], "favorites": df['fvcount'][4], "retweets": df['rtcount'][4], "tweet": df["tweet"][4]}}
    return data