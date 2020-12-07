import requests,os

os.chdir('C:\\Users\\Administrator\\Desktop\\CATIA临时文件\\Phython0\\网页')

res = requests.get('http://www.gutenberg.org/cache/epub/1112/pg1112.txt')

if res.status_code == requests.codes.ok:
	print('1')

	print(len(res.text))

	print(res.text[:250])
	
	#写入本地文件
	res.raise_for_status()
	playFile = open('RomeoAndJuliet.txt', 'wb')
	for chunk in res.iter_content(100000):
		playFile.write(chunk)

	playFile.close()
	
res = requests.get('http://inventwithpython.com/page_that_does_not_exist')
try:
	res.raise_for_status()
except Exception as exc:
	print('There was a problem: %s' % (exc))