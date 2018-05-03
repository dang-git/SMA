# -*- coding: utf-8 -*-
"""
Created on Wed May  2 17:14:46 2018

@author: franz.fangonilo
"""


import collections

def hash_(data):
    ls = []
    ls_ = []
    for i in data.tweet:
        text = i.lower().split(" ")
        for j in text:
            try:
                if j[0] == "#":
                    ls.append(j)
            except IndexError:
                next
    counter = collections.Counter(ls)
    top = counter.most_common(5)
    for i in top:
        ls_.append({"hashtag": i[0], "count": i[1]})
    return ls_