# -*- coding: utf-8 -*-
import pandas as pd
import time

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
    tl["int"] = [time.mktime(t.timetuple()) for t in tl.datehour]
    chartdata = {'x': tl["int"],
        'name': 'Volume', 'y1': tl['dateofposting'], 'kwargs1': { 'color': '#a4c639' }
    }
    return chartdata