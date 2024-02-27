import json
import re
from xml import etree
from fake_useragent import UserAgent


import html2text
import requests as requests
from bs4 import BeautifulSoup
from bs4.element import Comment, NavigableString
from urllib.parse import urlsplit, urlunsplit, urlparse

#from html2text.html2text import HTML2Text


#https://github.com/Alir3z4/html2text

#binary = FirefoxBinary('/usr/bin/firefox')
#browser = webdriver.Firefox(firefox_binary=binary)

#NEEDED TO SATISFY   https://stackoverflow.com/questions/28172008/pycharm-visual-warning-about-unresolved-attribute-reference




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
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


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

def params(soup, args):
    print('NA')
    #print(args[0])
    for arg in args:
        print(arg)
    for arg in args:
        key, value = arg

        if(value != 0):
            soupDecomp(soup.find_all(key, value))
        elif(key != None):
            soupDecomp(soup.find_all(key))

    return soup



def getArticle(url):
    urlNetLoc = urlparse(url).netloc
    soup = getSoup(url)


    if (urlNetLoc == 'www.foxnews.com'):

        divs = soup.find_all('div', {'class': "paywall"})

        if(len(divs) == 0):
            divs = soup.find_all('div', {'class': "article-body"})
        regex = re.compile('.*featured featured-video.*')
        soupDecomp(soup.find_all("div", {"class" : regex}))
        soupDecomp(soup.find_all('div', {'class':"article-gating-wrapper"}))
        soupDecomp(soup.find_all('span'))
        soupDecomp(soup.find_all('strong'))

    elif (urlNetLoc == 'www.cnn.com'):
        divs = soup.find_all('div', {'class': "article__content"})

        soupDecomp(soup.find_all('cite', class_="source__cite"))
        soupDecomp(soup.find_all('span'))
        soupDecomp(soup.find_all('div', {'class': "ad-feedback-link-container"}))


    elif(urlNetLoc == 'www.nbcnews.com'):
        divs = soup.find_all('div', {'class': "article-body__content"})
        if(len(divs) == 0):
            divs = soup.find_all('div', {'class': "wrapper"})
        if(len(divs) == 0):
            divs = soup.find_all('div', {'class': "video-details__dek"})


    elif(urlNetLoc == 'nypost.com'):

        divs = soup.find_all('div', {'class': "single__content"})

        soupDecomp(soup.find_all('aside',{"class": "single__inline-module"}))
        soupDecomp(soup.find_all('span', {'class': "nyp-slideshow-modal-image__icon-text"}))
        soupDecomp(soup.find_all('figcaption'))

    elif(urlNetLoc == 'abcnews.go.com'):
        divs = soup.find_all('div', {'data-testid': "prism-article-body"})

        if(len(divs) == 0):
            divs = soup.find_all('div', {'class': "video-info-module__text"})


    elif(urlNetLoc == 'www.vox.com'):
        divs = soup.find_all('div', {'class': "c-entry-content"})

    elif(urlNetLoc == 'www.theamericanconservative.com'):
        divs = soup.find_all('div', {'class': "c-blog-post__content"})

        soupDecomp(soup.find_all('div', {'class': "l-container"}))

    elif(urlNetLoc == 'spectator.org'):
        divs = soup.find_all('div', {'class': "post-body print-only"})
        regex = re.compile('.*perfect-pullquote.*')
        soupDecomp(soup.find_all("div", {"class" : regex}))

    else:
        return("0")

    return (divsToTxt(divs))





links = {"foxnews" : "https://www.foxnews.com/politics/who-tom-suozzi-look-democrat-flipped-santos-seat-blue",
         "cnn":"https://www.cnn.com/2024/02/07/politics/mike-johnson-house-republicans-impeachment/index.html",
         "nypost":"https://nypost.com/2024/02/11/sports/taylor-swift-celebrates-chiefs-super-bowl-2024-win-over-49ers/",
         "nbcnews":"https://www.nbcnews.com/specials/israel-hamas-war-spread-gaza-pakistan-middle-east-region/index.html",
         "abcnews":"https://abcnews.go.com/Technology/wireStory/baby-boom-african-penguin-chicks-hatches-san-francisco-107078610",
         "vox":"https://www.vox.com/politics/2024/2/13/24072287/lakewood-church-shooting-anti-trans-messaging",
         "theamericanconservative":"https://www.theamericanconservative.com/putin-supporter-covers-a-multitude-of-thought-crimes/",
         "":"",
         "":"",
         "":""

         #"yahoo":"https://news.yahoo.com/auburn-heisman-trophy-winner-awarded-004926887.html?guccounter=1"
         }

#print('NOW: ' + repr(getArticle(links.get("vox"))))

