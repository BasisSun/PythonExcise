# coding=utf-8
#! python3
# Downloads all the english images/pages for Dragonball Multiverse.

import requests
import os
import bs4

__author__ = "Shafqat Dulal"
__version__ = "1.0.0"

url = "https://www.dragonball-multiverse.com/cn/chapters.html?comic=page"
print(os.getcwd())
os.makedirs('/dbm', exist_ok=True)
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4'}

print("connectting....wait....")

# Find the last page, then work from there.
res = requests.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, features="lxml")
lastPageLink = soup.select('.chapters p a')[-1]
print("There are currently " + lastPageLink.text + " pages.")


StartPage = input("please input start page number:")

EndPage = 'page-' + input("please input end page number:")

url = "https://www.dragonball-multiverse.com/cn/page-" + StartPage+".html"

print(url)

lastPageFinished = False
presentPage = int(StartPage)

while lastPageFinished == False:

    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    imageElem = soup.select('#balloonsimg')
    if (len(imageElem) != 0):
        imageUrl = 'http://www.dragonball-multiverse.com' + \
            imageElem[0].get('src')

        print('Downloading image %s...,wait' % imageUrl)
        res = requests.get(imageUrl, headers=headers)
        res.raise_for_status()

        imageFile = open(os.path.join(os.getcwd(),
                                      '/dbm/', str(presentPage)+".jpg"), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

    else:
        print("cannot find image file! please check url")
        break

    if not (EndPage in url):
        nextLink = soup.select('a[rel="next"]')
        if(len(nextLink) != 0):
            url = "http://www.dragonball-multiverse.com" + nextLink[0].get('href')
            print(url)
            presentPage = presentPage+1
        else:
            lastPageFinished = True
    else:
        lastPageFinished = True
