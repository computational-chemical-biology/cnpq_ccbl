import twitter
import sqlalchemy as db
from api.tsv2msql import Tree_of_Life, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

nltk.download('stopwords')
nltk.download('punkt')

import json
import sys

engine = db.create_engine('sqlite:///api/tree_of_life.db')

stop_words=set(stopwords.words("english"))
ps = PorterStemmer()
lem = WordNetLemmatizer()

"""
Downloads all tweets from a given user.

Uses twitter.Api.GetUserTimeline to retreive the last 3,200 tweets from a user.
Twitter doesn't allow retreiving more tweets than this through the API, so we get
as many as possible.

t.py should contain the imported variables.
"""

#from t import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET


def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)
    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id
        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets
    return timeline

def word_list(text):
    text = re.sub('@\w+|https://.+|#\w+', '', text)
    tokenized_word = word_tokenize(text)
    stemmed_words=[]
    for w in tokenized_word:
        stemmed_words.append(ps.stem(w))
    filtered_words = []
    for w in stemmed_words:
        if w not in stop_words:
            filtered_words.append(w)
    #lem_words = [x.lower() for x in lem_words]
    filtered_words = [re.sub('[^\w\s]','', x) for x in filtered_words]
    return [x for x in list(set(filtered_words)) if x!='']

def print_cand(short_list):
    for c in short_list:
        print(c[1].text)

def query_db(term, print_query=False):
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    #query = session.query(Tree_of_Life).filter(Tree_of_Life.name == term)
    query = session.query(Tree_of_Life).filter(func.lower(Tree_of_Life.name).in_(term))
    '''
    t1 = time.time()
    df['name'].str.lower().isin(wl).any()
    t2 = time.time()
    t2-t1
    '''
    if print_query:
        for _row in query.all():
            print(_row.name, _row.uniqname)
    if query.first()!=None:
        return 1
    else:
        return 0

def update_journals(name, handle):
    with open('api/data/journals.json') as f:
        journals = json.load(f)
    journals[handle] = name
    with open('api/data/journals.json', 'w+') as f:
        json.dump(journals, f, indent=4)
    return 'Updated'

