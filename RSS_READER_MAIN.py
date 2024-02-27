import csv
import time

import feedparser
import pandas as pd
from pandas import *

#https://stackoverflow.com/questions/69276161/check-row-if-exist-in-csv-python
import csv

from Scraper import getArticle
from urllib.parse import urlsplit, urlunsplit, urlparse
col_names = ["RLPosition",
             "Body",
             "Link"]

def isNullOrWhiteSpace(str=None):
    return not str or str.isspace()
def checkAndAdd(rLPosition, body, link, sentDF):
    dict = {'RLPosition': [rLPosition], 'Body': [body], 'Link': [link]}
    Df2 = pd.DataFrame(dict)
    Df2 = pd.concat([sentDF, Df2[~Df2['Link'].isin(sentDF['Link'])]])
    return Df2


def rss_feed_append(url, dFrame):
    feed = feedparser.parse(url)

    for entry in feed.entries:

        if entry.link in dFrame.values:
            continue
        #cnn
        if "/live-news/" in entry.link:
            continue
        #ABC
        if "/Live/" in entry.link:
            continue

        if "pagesix.com" in entry.link:
            continue
        print(urlparse(entry.link).netloc)
        print(entry.link)
        body = getArticle(entry.link)
        #if(body is None or body == "0"):

        if(body == "0"):
            print("SKIP")
            continue

        print("Feed Title:", feed.feed.title)
        dFrame = checkAndAdd('6',body, entry.link, dFrame)
        print("Entry Title:", entry.title)
        print("Entry Link:", entry.link)
        print("Entry Published Date:", entry.published)
        print('\n')
    return dFrame
# List of RSS feed URLs

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

minute = 60

until_update = 15

while True:
    df = pd.read_csv("save_file.csv", names=col_names)
    for url in rss_feed_urls:
        df = rss_feed_append(url, df)
        df.to_csv('save_file.csv', index=False, quoting=csv.QUOTE_ALL, header=False)
    for i in range(until_update):
        print(str(int(i)) + " / " + str(until_update))
        time.sleep(minute)