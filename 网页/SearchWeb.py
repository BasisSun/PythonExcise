#! python3
# lucky.py - Opens several Google search results.
import requests, sys, webbrowser, bs4

ListOfWords=["tennis","ball"]
print('Googling...') # display text while downloading the Google page
res = requests.get('http://google.com/search?q=' + ' '.join(ListOfWords))#https://www.baidu.com/s?wd=sad&tn=62095104_3_oem_dg
res.raise_for_status()

# TODO: Retrieve top search result links.
soup = bs4.BeautifulSoup(res.text,'html.parser')

# TODO: Open a browser tab for each result.
linkElems = soup.select('.r a')

numOpen = min(3, len(linkElems))
for i in range(numOpen):
	webbrowser.open('http://google.com' + linkElems[i].get('href'))