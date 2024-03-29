import json
import re
from xml import etree
from fake_useragent import UserAgent


import html2text
import requests as requests
from bs4 import BeautifulSoup
from bs4.element import Comment, NavigableString
from urllib.parse import urlsplit, urlunsplit, urlparse

#NEEDED TO SATISFY   https://stackoverflow.com/questions/28172008/pycharm-visual-warning-about-unresolved-attribute-reference

def divsToTxt(divs):
    new = ''
    for i in range(0, len(divs)):
        new = new + html2text.html2text(divs[i].get_text(" "))

    new = new.replace("\n", " ")
    new = new.replace(' ', " ")
    return (new)

def soupDecomp(toRemove):
    for i in toRemove:
        if i:
            i.decompose()
#https://stackoverflow.com/questions/41792761/calling-and-using-an-attribute-stored-in-variable-using-beautifulsoup-4


def getSoup(url):
    ua = UserAgent()
    header = {'User-Agent':str(ua.chrome)}

    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "lxml")
    return(soup)




def getArticle(url):
    urlNetLoc = urlparse(url).netloc
    soup = getSoup(url)
    side = "0"

    if (urlNetLoc == 'www.foxnews.com'):

        divs = soup.find_all('div', {'class': "paywall"})

        if(len(divs) == 0):
            divs = soup.find_all('div', {'class': "article-body"})
        regex = re.compile('.*featured featured-video.*')
        soupDecomp(soup.find_all("div", {"class" : regex}))
        soupDecomp(soup.find_all('div', {'class':"article-gating-wrapper"}))
        soupDecomp(soup.find_all('span'))
        soupDecomp(soup.find_all('strong'))
        side = "1"

    else:
        return("0", 0)

    return (divsToTxt(divs), side)


print('NOW: ' + repr(getArticle("")))

