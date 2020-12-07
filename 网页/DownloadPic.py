import urllib.request
import re
import os
import logging
os.chdir('C:\\Users\\Administrator\\Desktop\\CATIA临时文件\\Phython0\\网页')

logging.disable(logging.CRITICAL)
logging.basicConfig(filename='myProgramLog.txt',level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')


def open_url(url):
	req=urllib.request.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36')
	page=urllib.request.urlopen(req)
	html=page.read().decode('utf-8')
	return html
	
def get_img(html):
	p=r'<img class=\"BDE_Image\".*?src="([^"]*\.jpg)".*?'
	imglist = re.findall(p,html)
	try:
		os.mkdir("NewPics")
		logging.debug('成功创建路径%s' % os.getcwd())
	except FileExistsError:
		#如果该文件夹已存在则覆盖保存！
		logging.debug('该文件夹已存在则覆盖保存%s' % os.getcwd())
		pass
	os.chdir("NewPics")
	for each in imglist:
		logging.debug('each='+each )
		filename = each.split("/")[-1]
		logging.debug('filename='+filename )
		urllib.request.urlretrieve(each,filename,None)
		
if __name__ == '__main__':
	url="http://tieba.baidu.com/p/3823765471"
	print('当前路径%s' % os.getcwd())
	get_img(open_url(url))