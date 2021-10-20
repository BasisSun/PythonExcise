#! python3
# Downloads all the english images/pages for Dragonball Multiverse.

import requests, os, bs4

__author__ = "Shafqat Dulal"
__version__ = "1.0.0"

url = "http://www.dragonball-multiverse.com/en/chapters.html"
os.makedirs('dbm', exist_ok=True)

# Find the last page, then work from there.
res = requests.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text)
lastPageLink = soup.select('.chapters p a')[-1]
print("There are currently " + lastPageLink.text + " pages.")
url = "http://www.dragonball-multiverse.com/en/" + lastPageLink.get('href')

lastPageFinished = False
while lastPageFinished == False:
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text)
    imageElem = soup.select('#balloonsimg img')
    if (len(imageElem) != 0):
        imageUrl = 'http://www.dragonball-multiverse.com' + soup.select('#balloonsimg img')[0].get('src')
        print('Downloading image %s...' % imageUrl)
        res = requests.get(imageUrl)
        res.raise_for_status()

        imageFile = open(os.path.join('dbm', os.path.basename(imageUrl)), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

    if not ('page-0' in url):
        prevLink = soup.select('a[rel="prev"]')[0]
        url = "http://www.dragonball-multiverse.com" + prevLink.get('href')
    else:
        lastPageFinished = True
