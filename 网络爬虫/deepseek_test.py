import requests
from bs4 import BeautifulSoup
import re
import time,random

#添加请求头
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

def get_page_content(url):
    response = requests.get(url,headers=headers)
    response.encoding = 'utf-8'
    return response.text

def extract_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # 提取标题
    title_tag = soup.find('div', class_='bookname').find('h1')
    title = title_tag.get_text().strip()
    
    # 提取正文
    content_tag = soup.find('div', id='content')
    un_clean_text = content_tag.get_text().strip()
    
    # 使用正则表达式将连续的多个\xa0字符替换为单个换行符\n
    content = re.sub(r'\xa0+', '\n', un_clean_text)
    # 将正文中的\r\n换成一个\n
    content = re.sub(r'\r\n+', '\n', content)
    
    # 去除多余的说明字符
    start_marker = "最新网址：www.35wx.la"
    end_marker = "最新网址：www.35wx.la"
    
    start_index = content.find(start_marker) + len(start_marker)
    end_index = content.find(end_marker, start_index)
    
    cleaned_content = content[start_index:end_index].strip()
    
    return title, cleaned_content

def get_next_page_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    next_page_tag = soup.find('a', string=re.compile(r'下一页|下一章'))
    
    if next_page_tag:
        return next_page_tag['href']
    else:
        return None

def save_to_file(title, content, filename):
     # 判断当前页码是否为1
    is_first_page = False
    page_info = re.search(r'\((\d+)/(\d+)\)', title)
    if page_info:
        current_page = int(page_info.group(1))
        is_first_page = (current_page == 1)
        

    with open(filename, 'a', encoding='utf-8') as file:
        if is_first_page:
            if '节' in title:
                file.write(f"\r\n第{title.split('节')[0]}节 {title.split('节')[1].split('(')[0].strip()}\r\n")
            else:
                # print(page_info.span())
                ajust_title = title[0:page_info.span()[0]].strip()
                if ' ' in ajust_title:
                    list_str = ajust_title.split(' ')
                    file.write(f"\r\n{list_str[0]}节 {list_str[1]}\r\n")
                else:
                    file.write(f"\r\n{title[0:page_info.span()[0]]}\r\n")#

        file.write(content)

def main():
    base_url = "https://www.35wx.la/9_9319/"
    current_url = "https://www.35wx.la/9_9319/43138350.html"
    output_file = "临高启明.txt"
    
    while current_url:
        print(f"正在爬取: {current_url}")
        html = get_page_content(current_url)

        retry = 0 #重复读取某一网址次数
        while retry < 3:
            try:
                title, content = extract_content(html)
                print(f"查找到标题: {title}")
                break
            except Exception as e:
                retry +=1
                print(f"网页有误，未成功找到正文内容，{e}，重试第{retry}次。。")
                time.sleep(2)
                
        if retry >=3:
            print("未能找到下一页有效界面了，请手动重试.")

        # 随机3-5秒时延
        delay = random.randint(3,5)
        time.sleep(delay)

        save_to_file(title, content, output_file)
        
        next_page_url = get_next_page_url(html)

        if next_page_url == None:
            print("没有下一页，已经结束")
            break
        
        if next_page_url:
            if next_page_url.startswith('/'):
                next_page_url = next_page_url.split('/')[-1]
            next_page_url = base_url + next_page_url
            # user_input = input("是否继续爬取下一页？(y/n): ").strip().lower()
            # if user_input == 'y':
            current_url = next_page_url
            # else:
            #     break
        else:
            print("已到达最后一页，爬取结束。")
            break

if __name__ == "__main__":
    main()
