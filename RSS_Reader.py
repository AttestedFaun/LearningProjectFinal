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
            #"Published",
            #"Summary"]
#df = pd.read_csv("save_file.csv", names=col_names)

def isNullOrWhiteSpace(str=None):
  return not str or str.isspace()
def checkAndAdd(rLPosition, body, link, sentDF):
    dict = {'RLPosition': [rLPosition], 'Body': [body], 'Link': [link]}
    Df2 = pd.DataFrame(dict)
    Df2 = pd.concat([sentDF, Df2[~Df2['Link'].isin(sentDF['Link'])]])
    return Df2

#def fetch_rss_data():
    #feed_data = pd.read_csv("save_file.csv", index_col="id", usecols=col_names)
# List of RSS feed URLs

def rss_feed_append(url, dFrame):
    feed = feedparser.parse(url)


    #print("Feed Title:", feed.feed.title)



    for entry in feed.entries:

        if entry.link in dFrame.values:
            #print('EXISTS:                   ' + entry.link )
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
        body, side = getArticle(entry.link)
        #print(entry.link)
        #if(body is None or body == "0"):
        print("body: " + body)

        #"""
        if(body == "0"):
            print(body)
            #print("skip")
            print("SKIP")
            continue
        #"""

        print("Feed Title:", feed.feed.title)
        dFrame = checkAndAdd(side ,body, entry.link, dFrame)
        #print(dFrame)
        #print("Entry Text: " + entry.text)
        print("Entry Title:", entry.title)
        print("Entry Link:", entry.link)
        print("Entry Published Date:", entry.published)
        #print("Entry Summary:", entry.summary)
        #print("Entry Content:", entry.content)
        print("\n")
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
#http://rss.cnn.com/rss/cnn_latest.rss
#https://moxie.foxnews.com/google-publisher/latest.xml
# Fetch data from multiple RSS feeds
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


















"""
#save_writer.writerow(['2', 'Accounting', 'November'])
person = ['1', '2', '2']
style = ['one', 'IT', 'March']
month = ['March', 'November', 'March']
dict = {'Position': person, 'Link': style, 'C': month}
df = pd.DataFrame(dict)
# saving the dataframe
df.to_csv('save_file.csv', index=False, quoting=csv.QUOTE_ALL, header=False)

person = ['1', '2', '2']
style = ['one', 'womp', 'March']
month = ['March', 'cong', 'March']
dict = {'Position': person, 'Link': style, 'C': month}
Df2 = pd.DataFrame(dict)
Df2 = pd.concat([df, Df2[ ~Df2['Link'].isin(df['Link'])] ])
Df2.to_csv('save_file.csv', index=False, quoting=csv.QUOTE_ALL, header=False)
"""