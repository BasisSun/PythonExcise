import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup

def main():
	# url = "http://baike.baidu.com/view/284853.htm"
	# response=urllib.request.urlopen(url)
	# html = response.read()
	# soup = BeautifulSoup(html,"html.parser")
	
	# for each in soup.find_all(href=re.compile("view")):
		# print(each.text,"->",''.join(["http://baike.baidu.com",each["href"]]))
	keywords = input("请输入关键词：")
	keywords = urllib.parse.urlencode({"word":keywords})
	response=urllib.request.urlopen("http://baike.baidu.com/search/words? %s" % keywords)
	html=response.read()
	soup=BeautifulSoup(html,"html.parser")
	
	for each in soup.find_all(hrep = re.compile("view")):
		content = ''.join([each.text])
		url2= ''.join(["http://baike.baidu.com",each["href"]])
		response2=urllib.request.urlopen(url2)
		html2=response2.read()
		soup2=BeautifulSoup(html2,"html.parser")
		if soup2.h2:
			content=''.join([content,soup2.h2.text])
		content = ''.join([content,"->",url2])
		print(content)
		
if __name__=="__main__":
	main()