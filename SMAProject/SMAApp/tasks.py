from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
from SMAApp import lda, engagements, hashtags, globals
import pandas as pd

@task
def generate_lda_data(df):
    print("lda started")
    data = pd.read_json(df)
    lda_data = lda.lda_model(data)
    return lda_data

@task
def generate_sentiments_data(df):
    print("polar started")
    data = pd.read_json(df)
    sentiments = engagements.return_polarity_chartdata(data)
    #polarityTable = engagements.return_polarity(data)
    print("polar end")
    return sentiments #int(polarityTable)

@task
def prepareChartData(df):
    print("preparing chart data")
    data = pd.read_json(df)
    barchartData = hashtags.hash_(data)
    return barchartData