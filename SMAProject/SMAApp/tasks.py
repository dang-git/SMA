from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
from SMAApp import lda, engagements, hashtags, wordcloudscript
import pandas as pd

@task
def generate_lda_data(num_topics, df):
    print("lda started")
    data = pd.read_json(df)
    lda_data = lda.lda_model(num_topics,data)
    return lda_data

@task
def generate_sentiments_data(df):
    print("polar started")
    data = pd.read_json(df)
    sentiments = engagements.return_polarity_chartdata(data)
    #polarityTable = engagements.return_polarity(data)
    print("polar end")
    return sentiments #int(polarityTable)

# @task
# def generate_wordcloud_image(df):
#     print("Image creation started")
#     img_str = wordcloudscript.return_wordcloud(df)
#     return img_str
@task
def prepareChartData(df):
    print("preparing chart data")
    data = pd.read_json(df)
    barchartData = hashtags.hash_(data)
    return barchartData