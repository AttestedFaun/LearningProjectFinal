import csv
from urllib.parse import urlsplit, urlunsplit, urlparse
import feedparser
import pandas as pd
from fastpunct import FastPunct

import numpy as np
#https://stackoverflow.com/questions/75367803/how-to-remove-spaces-in-a-single-word-bo-ok-to-book

import enchant

def formattingTool(text):
    #text = "int ernational trade is not good for economies"
    text = str(text)
    fixed_text = []

    d = enchant.Dict("en_US")

    for i in range(len(words := text.split())):
        if fixed_text and not d.check(words[i]) and d.check(compound_word := ''.join([fixed_text[-1], words[i]])):
            fixed_text[-1] = compound_word
        else:
            fixed_text.append(words[i])

    #print(' '.join(fixed_text))\
    fixed_text = str(' '.join(fixed_text))

    #fastpunct = FastPunct()
    #print(fastpunct.punct(fixed_text))
    #return(fastpunct.punct(fixed_text))
    return(fixed_text)

rss_feed_urls = [
    "https://nypost.com/feed/",
    "https://feeds.nbcnews.com/nbcnews/public/news",
    "http://rss.cnn.com/rss/cnn_latest.rss",
    "https://moxie.foxnews.com/google-publisher/latest.xml",
    "https://www.vox.com/rss/index.xml",
    "https://www.theamericanconservative.com/feed/",
    "http://abcnews.go.com/abcnews/topstories",
    "https://spectator.org/feed/"
]


col_names = ["RLPosition",
             "Body",
             "Link"]


df = pd.read_csv("save_file_UNORGANIZED.csv", names=col_names)
"""
df['Link'] = df['Link'].apply(
    lambda x:urlparse(x).netloc if urlparse(x).netloc == 'www.foxnews.com' or
                  urlparse(x).netloc == 'nypost.com' or
                  urlparse(x).netloc == 'www.theamericanconservative.com' or
                  urlparse(x).netloc == 'spectator.org' else (
        urlparse(x).netloc if urlparse(x).netloc == 'www.cnn.com' or
             urlparse(x).netloc == 'www.nbcnews.com' or
             urlparse(x).netloc == 'abcnews.go.com' or
             urlparse(x).netloc == 'www.vox.com' else None
    )
)
"""
df['Link'] = df['Link'].apply(
    lambda x:urlparse(x).netloc
)

df['Body'] = df['Body'].apply(
    lambda x:formattingTool(x)
)


df['RLPosition'] = df['Link'].apply(
    lambda x:1 if x == 'www.foxnews.com' or
                  x == 'nypost.com' or
                  x == 'www.theamericanconservative.com' or
                  x == 'spectator.org' else (
        2 if x == 'www.cnn.com' or
             x == 'www.nbcnews.com' or
             x == 'abcnews.go.com' or
             x == 'www.vox.com' else None
    )
)
print(df)
#Drop List
dfTRAIN = df[~df[['Link']].isin(['www.vox.com', 'spectator.org']).any(axis=1)]
dfTEST = df[~df[['Link']].isin(['www.foxnews.com', 'nypost.com','www.theamericanconservative.com','www.cnn.com', 'www.nbcnews.com', 'abcnews.go.com']).any(axis=1)]

dfTRAIN = dfTRAIN.drop('Link', axis=1)
dfTEST = dfTEST.drop('Link', axis=1)

dfTRAIN.to_csv('save_file_TRAIN.csv', index=False, quoting=csv.QUOTE_ALL, header=False)
dfTEST.to_csv('save_file_TEST.csv', index=False, quoting=csv.QUOTE_ALL, header=False)
#df.to_csv('save_file_TRAIN.csv', index=False, quoting=csv.QUOTE_ALL, header=False)