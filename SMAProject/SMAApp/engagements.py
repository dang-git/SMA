# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime

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

#def 