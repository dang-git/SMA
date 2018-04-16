# -*- coding: utf-8 -*-


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