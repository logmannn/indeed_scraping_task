#! /usr/bin/python

import requests
from lxml import html
from lxml import cssselect

csvFilename = "besmith_scraping.csv"
csv = open(csvFilename, "w")
colNames = "Titles, URLs, Locations\n"
csv.write(colNames)

link = 'https://www.besmith.com/candidates/search-listings?page='
desiredPage = '2'

currentPage = 1
morePages = 'true'

while morePages == 'true':
    if desiredPage == str (currentPage):
        currentPage = desiredPage

    if desiredPage == '' or desiredPage == str (currentPage):
        print(currentPage)

        response = requests.get(link + str (currentPage))
        sourceCode = response.content
        htmlElem = html.document_fromstring(sourceCode)

        jobs = htmlElem.cssselect('.job-list__item div:first-child')
        for elem in jobs:
            title = elem.cssselect('a.h2 span')[0].text_content().replace(',', '-')
            url = elem.cssselect('a.h2')[0].get('href').replace(',', '-')
            location = ' '.join(elem.cssselect('h4')[0].text_content().replace(',', '-').split())

            csv.write(title + ',' + 'https://www.besmith.com'+url + ',' + location + '\n')

        lastPageButton = htmlElem.cssselect('.last')
        if lastPageButton == [] or desiredPage == str (currentPage):
            morePages = 'false'
        else:
            currentPage += 1
    else:
        currentPage += 1
