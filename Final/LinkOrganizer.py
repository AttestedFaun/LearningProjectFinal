import csv
from urllib.parse import urlsplit, urlunsplit, urlparse
import feedparser
import pandas as pd
import numpy as np
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

df['RLPosition'] = df['Link'].apply(
    lambda x:1 if urlparse(x).netloc == 'www.foxnews.com' or
                  urlparse(x).netloc == 'nypost.com' or
                  urlparse(x).netloc == 'www.theamericanconservative.com' or
                  urlparse(x).netloc == 'spectator.org' else (
        2 if urlparse(x).netloc == 'www.cnn.com' or
             urlparse(x).netloc == 'www.nbcnews.com' or
             urlparse(x).netloc == 'abcnews.go.com' or
             urlparse(x).netloc == 'www.vox.com' else None
    )
)
df = df.drop('Link', axis=1)
df.to_csv('save_file_TRAIN.csv', index=False, quoting=csv.QUOTE_ALL, header=False)