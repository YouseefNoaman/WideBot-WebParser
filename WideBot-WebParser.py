# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 19:33:00 2019

@author: SefoNoaman
"""

import re
import requests
from bs4 import BeautifulSoup
import sys
import time

URLS = []  # a list to hold the URLs to check if there is a duplicate


def waitForThirty():  # this function will be used to make a 30 seconds interval
    time.sleep(2)


def getLink(url):
    response = requests.get(url)
    print("response", response)
    html = response.text
    print("html", html)
    soup = BeautifulSoup(html, "html.parser")

    # print(soup)

    link = soup.find('p')
    print(link)
    article_link = link.find("a", attrs={'href': re.compile("^/wiki/")})
    print(article_link)
    return article_link


def find_philosophy(url):
    MAX_HOPS = 100
    count = 0

    link = getLink(url)
    print(link)

    while '/wiki/Philosophy' not in link:
        if count == MAX_HOPS:
            print("MAX_HOPS reached.")
            return None

        link = getLink(link)
        count = count + 1

        waitForThirty()
        if isDuplicate(link, URLS):
            print("we are in a loop")

    print(str(count) + " hops")
    return count


#


def isDuplicate(URL,
                URLs):  # this function should check if the url is visited before, so it means we are stuck in a loop
    if URL in URLs:
        return True
    else:
        return False


if __name__ == '__main__':  # this is used to run the code internally, to also import the file and use it by other people
    urlRandom = 'http://en.wikipedia.org/wiki/Special:Random'

    # sys.argv is automatically a list of strings representing the arguments, to get the number of them use len()
    if len(sys.argv) == 1:  # if no arguments, use random Wikipedia page
        print("Using http://en.wikipedia.org/wiki/Special:Random")
        url = urlRandom
    else:
        url = sys.argv[1]

    find_philosophy(url)
