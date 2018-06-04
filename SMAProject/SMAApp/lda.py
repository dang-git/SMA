# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 11:10:23 2018

@author: franz.fangonilo
"""
 
import nltk
from gensim import corpora, models
import re
import json
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
lemma = nltk.wordnet.WordNetLemmatizer()
from django.conf import settings
import pyLDAvis
import pyLDAvis.gensim
import os.path

stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(["rt", "n't", "'s", "ve", "amp"])

#def replace_unicodes(text): 
#    for i in unicode_chars:
        #text = str(text.encode('utf-8')).replace(i, "")[2:-1]
#        text = text.encode('utf-8').decode('ascii', 'ignore')
#    return text

def tokenize_only(text):
    text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', str(text))
    text = text.encode('utf-8').decode('ascii', 'ignore')
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    filtered_tokens = " ".join(filtered_tokens)
    return filtered_tokens

def tokenize_and_stem(text):
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    # there is a need to improve stemmer
    stems = [lemma.lemmatize(t) for t in filtered_tokens]
    return stems

def further_process(sentences):
    preprocess = [tokenize_only(doc) for doc in sentences]
    texts = [tokenize_and_stem(text) for text in preprocess]
    texts = [[word for word in text if word not in stopwords] for text in texts]
    dictionary = corpora.Dictionary(texts)
    dictionary.filter_extremes(no_below=1, no_above=0.8)
    corpus = [dictionary.doc2bow(text) for text in texts]
    return corpus, dictionary

def lda_model(data):
    corpus, dictionary = further_process(data.tweet)
    lda = models.LdaModel(corpus, num_topics=4, id2word=dictionary, update_every=5,
                          chunksize=10000, passes=100)
    topics_matrix = lda.show_topics(formatted=False, num_words=20)
    all_topics = {}
    for i in topics_matrix:
        topic = []
        for j in i[1]:
            topic.append(j[0])
        all_topics[len(all_topics)+1] = ", ".join(topic)
    p = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    # get data as json
    lda_data = json.dumps(p.to_dict())
    return lda_data
    # filename = "lda-" + sessionid + ".html"
    #path = "C:/Users/christian.dy/Documents/GitHub/SMALab/SMAProject/SMAApp/templates/lda/"
    # ldaPath = os.path.join(settings.BASE_DIR, "SMAApp\\templates\\lda\\" + filename)
    # pyLDAvis.save_html(p, ldaPath)
    #return all_topics