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
    time.sleep(30)


def find_philosophy(url):
    MAX_HOPS = 100  # maximum number of clicks on links
    count = 0  # number of hops

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")  # souping the URL up and converting it to text using beautifulsoup
    print(r.url)  # Print current url (after redirection)
    URLS.append(r.url)
    # the souping isn't working here, i think maybe Wikipedia stopping scraping by bots maybe, so i guess selenium
    # should be used instead but there is no time for further modification
    soup = soup.find("span", id='firstHeading')
    soup = soup.text
    print(soup)
    while soup != 'Philosophy':
        if count == MAX_HOPS:
            print("MAX_HOPS reached.")
            return None

        content = soup.find(id='mw-content-text')
        for t in content.find_all(class_=['navbox', 'vertical-navbox', 'toc']):
            t.replace_with("")

        paragraph = soup.select('div#mw-content-text > p')[0]  # Only DIRECT child
        for s in paragraph.find_all(
                ['span', 'small', 'sup,', 'i', 'table']):  # remove spans and smalls with language, pronounciation
            s.replace_with("")
        paragraphText = str(paragraph)
        paragraphText = re.sub(r' \(.*?\)', '', paragraphText)  # Remove leftover parenthesized text

        # For debugging:
        # print(paragraphText)

        reParagraph = BeautifulSoup(paragraphText)  # back into bs4 object to find links
        firstLink = reParagraph.find(href=re.compile('^/wiki/'))  # links that start with /wiki/ only

        while firstLink == None:
            # case of disambiguation: use first wiki link in list
            if '(disambiguation)' in url or '(surname)' in url:
                firstLink = content.ul.find(href=re.compile('^/wiki/'))

            else:
                paragraph = paragraph.find_next_sibling("p")

                if paragraph is None:  # Catch-case

                    if content.ul is not None:  # means if the scanned links in page has content
                        firstLink = content.ul.find(href=re.compile('^/wiki/'))  # Disambiguation-type page
                    if firstLink is None:  # No links available
                        print("Wikipedia not reachable.")
                        return None
                    continue

                for s in paragraph.find_all(['span', 'small', 'sup,', 'i', 'table']):
                    s.replace_with("")
                paragraphText = str(paragraph)
                paragraphText = re.sub(r' \(.*?\)', '', paragraphText)
                reParagraph = BeautifulSoup(paragraphText)
                firstLink = reParagraph.find(href=re.compile('^/wiki/'))

            # For debugging:
            # print(paragraphText)

        url = 'http://en.wikipedia.org' + firstLink.get('href')
        print(url)
        r = requests.get(url)  # Make new request
        soup = BeautifulSoup(r.text)  # Soup it up again

        count = count + 1

        waitForThirty()
        if isDuplicate(r.url, URLS):
            print("we are in a loop")
            break;

    print(str(count) + " hops")
    return count


def isDuplicate(URL,
                URLs):  # this function should check if the url is visited before, so it means we are stuck in a loop
    if URL in URLs:
        return True
    else:
        return False


if __name__ == '__main__':
    urlRandom = 'http://en.wikipedia.org/wiki/Special:Random'

    # sys.argv is automatically a list of strings representing the arguments, to get the number of them use len()
    if len(sys.argv) == 1:  # if no arguments, use random Wikipedia page
        print("Using http://en.wikipedia.org/wiki/Special:Random")
        url = urlRandom
    else:
        url = sys.argv[1]

    find_philosophy(url)
