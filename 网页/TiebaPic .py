#import urllib.request
import requests
import bs4
import re
import os
import logging
os.chdir('C:\\Users\\Administrator\\Desktop\\CATIA临时文件\\Phython0\\网页')

logging.disable(logging.CRITICAL)
logging.basicConfig(filename='myProgramLog.txt',level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

requestSession = requests.session()
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
requestSession.headers.update({'User-Agent': UA})

def open_url(url):

	req=requestSession.get(url)
	
	req.raise_for_status()
	
	logging.debug(req.text)
	soup = bs4.BeautifulSoup(req.text,'html.parser')
	return soup
	
def get_img(soup):
	#p=r'<img class=\"BDE_Image\".*?src="([^"]*\.jpg)".*?'
	#imglist = soup.find_all("img", class_="BDE_Image")
	#imglist = soup.find_all(class_="pic-box-item",attrs={"data-img": re.compile("\.gif$")})
	imglist = soup.select(".pic-box-item")
	#imglist = soup.find_all('img',attrs={"data-origin-src": re.compile("\.jpg$")})
	print(imglist)
	try:
		os.mkdir("NewPics")
		logging.debug('成功创建路径%s' % os.getcwd())
	except FileExistsError:
		#如果该文件夹已存在则覆盖保存！
		logging.debug('该文件夹已存在则覆盖保存%s' % os.getcwd())
		pass
	os.chdir("NewPics")
	for each in imglist:
		#logging.debug('each='+each.text)
		fileSrc=each["data-img"]
		print(fileSrc)
		
		res = requests.get(fileSrc)
		res.raise_for_status()
		
		filename = fileSrc.split("/")[-1]
		logging.debug('filename='+filename )
		
		# TODO: Save the image to ./xkcd.
		imageFile = open(filename, 'wb')#
		for chunk in res.iter_content(100000):
			imageFile.write(chunk)
		imageFile.close()

		
if __name__ == '__main__':
	url="http://tu.duowan.com/scroll/136635.html"
	print('当前路径%s' % os.getcwd())
	get_img(open_url(url))