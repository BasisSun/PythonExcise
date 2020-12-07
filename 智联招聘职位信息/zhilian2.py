#-*- coding: utf-8 -*-
'''
Created on 2018-05-7
@author: Vinter_he
'''
import re
import requests
import xlwt
from tqdm import tqdm
from urllib.parse import urlencode
from requests.exceptions import RequestException
from lxml import etree
import user_agents
import random
import datetime
import os

os.chdir('E:\\Python0\\智联招聘职位信息')
    
def get_one_page(city, keyword, region, page):
   '''
   获取网页html内容并返回
   '''
   paras = {
       'jl': city,         # 搜索城市
       'kw': keyword,      # 搜索关键词
       'isadv': 0,         # 是否打开更详细搜索选项
       'isfilter': 1,      # 是否对结果过滤
       'p': page,          # 页数
       're': region        # region的缩写，地区，2005代表海淀
   }
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
       'Host': 'sou.zhaopin.com',
       'Referer': 'https://www.zhaopin.com/',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
       'Accept-Encoding': 'gzip, deflate, br',
       'Accept-Language': 'zh-CN,zh;q=0.9'
   }
   url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?' + urlencode(paras)
   try:
       # 获取网页内容，返回html数据
       response = requests.get(url, headers=headers)
       # 通过状态码判断是否获取成功
       if response.status_code == 200:
           return response.text
       return None
   except RequestException as e:
       return None
def parse_one_page(html):
   '''
   解析HTML代码，提取有用信息并返回
   '''
   # 正则表达式进行解析
   pattern = re.compile('<a style=.*? target="_blank">(.*?)</a>.*?'        # 匹配职位信息
       '<td class="gsmc"><a href="(.*?)" target="_blank">(.*?)</a>.*?'     # 匹配公司网址和公司名称
       '<td class="zwyx">(.*?)</td>', re.S)                                # 匹配月薪
   # 匹配所有符合条件的内容
   items = re.findall(pattern, html)
   for item in items:
       job_name = item[0]
       job_name = job_name.replace('<b>', '')
       job_name = job_name.replace('</b>', '')
       yield {
           0: job_name,
           1: item[1],
           2: item[2],
           3: item[3]
       }
# 存入excle
def write_xls_file(filename, headers, jobs):
    table = xlwt.Workbook(encoding='utf8')
    table_page = table.add_sheet('jobs')
    for i,header in enumerate(headers):
        table_page.write(0,i,header)
    for j,items in enumerate(jobs,start = 1):
        for q,item in items.items():
            table_page.write(j, q, item)
    table.save(filename)
def main(city, keyword, region, pages):
   '''
   主函数
   '''
   filename = '智联_' +datetime.date.today().strftime('%Y-%m-%d')+ city + '_' + keyword + '.xls'
   headers = ['job', 'website', 'company', 'salary']
   jobs = []
   for i in tqdm(range(pages)):
       '''
       获取该页中所有职位信息，写入xls文件
       '''
       region = parseHtmlToGetRegion(region)
       html = get_one_page(city, keyword, region, i)
       items = parse_one_page(html)
       for item in items:
           jobs.append(item)
   write_xls_file(filename, headers, jobs)
def getHtml(url):
    response = requests.get(url=url, headers={'User-Agent':random.choice(user_agents.user_agents)}, timeout=10).text
    html = etree.HTML(response)
    return html
# 取搜索页面得到地域的对应数字 比如海淀对应2005
def parseHtmlToGetRegion(regionAddress):
    url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=北京&sm=0&isfilter=1&p=1&re=2006'
    # 获取代理ip地址 只取前五页
    html= getHtml(url)
    regionId = html.xpath('/html/body/div[3]/div[3]/div[1]/div[4]/div[1]/div[2]/a/@href')
    region = html.xpath('/html/body/div[3]/div[3]/div[1]/div[4]/div[1]/div[2]/a/text()')
    #解析一下region中的编号去掉无效内容
    regionList = {}
    for i,regionHref in enumerate(regionId):
        if i==0:
            continue
        regionList[region[i]] = regionId[i][-4::]
    return regionList.get(regionAddress)
if __name__ == '__main__':
   main('北京', 'php工程师', '朝阳', 10)