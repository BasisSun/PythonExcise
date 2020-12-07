import requests, bs4,os
os.chdir('C:\\Users\\Administrator\\Desktop\\CATIA临时文件\\Phython0\\网页')
#res = requests.get('http://nostarch.com')

#本地文件
#exampleFile = open('example.html')

#res.raise_for_status()
#noStarchSoup = bs4.BeautifulSoup(res.text)
#type(noStarchSoup)

exampleFile = open('example.html')
exampleSoup = bs4.BeautifulSoup(exampleFile.read(),'html.parser')
elems = exampleSoup.select('#author')
print(type(elems))

print(len(elems))

print(type(elems[0]))

print(elems[0].getText())

print(str(elems[0]))

print(elems[0].attrs)

pElems = exampleSoup.select('p')
print(str(pElems[0]))

print(pElems[0].getText())

print(str(pElems[1]))

print(pElems[1].getText())

print(str(pElems[2]))

print(pElems[2].getText())


soup = bs4.BeautifulSoup(open('example.html'),'html.parser')
spanElem = soup.select('span')[0]
print(str(spanElem))

print(spanElem.get('id'))

print(spanElem.attrs)
