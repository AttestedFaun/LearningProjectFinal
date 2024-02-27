import json
import re

import feedparser
import html2text
import requests as requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from bs4.element import Comment, NavigableString
from urllib.parse import urlsplit, urlunsplit, urlparse

from selenium.webdriver.firefox.service import Service
import urllib.request
from lxml.html import fromstring, unicode
#https://github.com/Alir3z4/html2text

#binary = FirefoxBinary('/usr/bin/firefox')
#browser = webdriver.Firefox(firefox_binary=binary)


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(string=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

"""
# define the function blocks
def zero():
    print "You typed zero.\n"

def sqr():
    print "n is a perfect square\n"

def even():
    print "n is an even number\n"

def prime():
    print "n is a prime number\n"

# map the inputs to the function blocks
options = {0 : zero,
           1 : sqr,
           4 : sqr,
           9 : sqr,
           2 : even,
           3 : prime,
           5 : prime,
           7 : prime,
}
"""





#url = 'https://nypost.com/2024/01/31/entertainment/wheel-of-fortune-player-robbed-of-40k-prize-for-puzzle-clearly-solved-fans-cry-in-online-outrage/'
#url = 'https://www.nbcnews.com/politics/congress/lawmakers-press-biden-get-congress-approval-middle-east-airstrikes-rcna136206'



def getArticle(url):
    if (urlparse(url).netloc == 'www.foxnews.com'):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        divs = soup.find_all('div', {'class': "paywall"})

        toRemove = soup.find_all('div', class_="article-gating-wrapper")
        for i in toRemove:
            if i:
                i.decompose()


        toRemove = soup.find_all('strong')
        for i in toRemove:
            if i:
                i.decompose()


        toRemove = soup.find_all('span')
        for i in toRemove:
            if i:
                i.decompose()

        new = ''
        for i in range(0, len(divs)):
            removeHTML = BeautifulSoup(divs[i].get_text(separator="").strip(), 'lxml')

            lineOfArticleList = list(removeHTML.text)

            for x in range(len(lineOfArticleList)):
                if (lineOfArticleList[x] == ' ' and lineOfArticleList[x-1] == ' '):
                    continue
                elif (lineOfArticleList[x].isprintable()):
                    new = new + lineOfArticleList[x]
        return (new)


    if (urlparse(url).netloc == 'www.cnn.com'):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        divs = soup.find_all('div', {'class': "article__content"})
        toRemove = soup.find_all('cite', class_="source__cite")
        for i in toRemove:
            if i:
                i.decompose()
        toRemove = soup.find_all('span')
        for i in toRemove:
            if i:
                i.decompose()
        toRemove = soup.find_all('div', {'class': "ad-feedback-link-container"})
        for i in toRemove:
            if i:
                i.decompose()

        mua = ''

        new = ''
        for i in range(0, len(divs)):
            #print(divs[i])
            mua = mua + html2text.html2text(divs[i].text)
            mua = mua.replace("\n", " ")
            for x in range(len(mua)):
                if (mua[x] == ' ' and mua[x-1] == ' '):
                    continue
                elif (mua[x].isprintable()):
                    new = new + mua[x]

        """
            removeHTML = BeautifulSoup(divs[i].get_text(separator=' ').strip(), 'lxml')
            #print(removeHTML)

            lineOfArticleList = list(removeHTML.text)

            for x in range(len(lineOfArticleList)):
                if (lineOfArticleList[x] == ' ' and lineOfArticleList[x-1] == ' '):
                    continue
                elif (lineOfArticleList[x].isprintable()):
                    new = new + lineOfArticleList[x]
        new1 = ""
        for x in range(len(new)):
            if (new[x] == ' ' and new[x-1] == ' '):
                continue
            elif (new[x].isprintable()):
                new1 = new1 + new[x]
        """
        return (mua)
        #return('0')






    if(urlparse(url).netloc == 'www.nbcnews.com'):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        divs = soup.find_all('div', {'class': "article-body__content"})

        new = ''
        for i in range(0, len(divs)):
            lineOfArticleList = list(divs[i].text)
            for x in range(len(lineOfArticleList)):
                if (lineOfArticleList[x].isprintable()):
                    new = new + lineOfArticleList[x]

        return(new)


    if(urlparse(url).netloc == 'nypost.com'):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        divs = soup.find_all('div', {'class': "single__content"})

        toRemove = soup.find('aside', class_="single__inline-module")
        if toRemove:
            toRemove.decompose()

        for i in range(0, len(soup.find_all('span', class_="nyp-slideshow-modal-image__icon-text"))):
            soup.find('span', class_="nyp-slideshow-modal-image__icon-text").decompose()

        new = ''
        for i in range(0, len(divs)):
            lineOfArticleList = list(divs[i].text)
            for x in range(len(lineOfArticleList)):
                if (lineOfArticleList[x].isprintable()):
                    new = new + lineOfArticleList[x]
        return(new)
    return("0")

#print('NOW: '+ getArticle('https://www.foxnews.com/us/ice-nabs-illegal-immigrants-alaska-washington-state-oregon-texas-convictions-child-exploitation'))
print('NOW: ' + getArticle('https://www.cnn.com/2024/02/07/politics/mike-johnson-house-republicans-impeachment/index.html'))