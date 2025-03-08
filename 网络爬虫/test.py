import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def crawl_novel(start_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    current_url = start_url
    output_file = 'novel_content.txt'

    # 初始化文件（如果存在先清空）
    if os.path.exists(output_file):
        open(output_file, 'w').close()

    while True:
        try:
            # 发送HTTP请求
            response = requests.get(current_url, headers=headers)
            response.encoding = 'utf-8'
            response.raise_for_status()

            # 解析网页内容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取正文内容
            content_div = soup.find('div', {'id': 'content'})
            if not content_div:
                print("未找到正文内容！")
                break
                
            # 清理内容并保存
            content = content_div.get_text('\n', strip=True)
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(content + '\n\n')
            
            # 查找下一页链接
            next_page = None
            for a_tag in soup.find_all('a'):
                if '下一页' in a_tag.text:
                    next_page = a_tag.get('href')
                    break

            if not next_page:
                print("已到达最后一页！")
                break

            # 构建完整URL
            next_url = urljoin(current_url, next_page)
            
            # 用户交互
            choice = input(f"当前页面：{current_url}\n是否继续爬取下一页？(y/n): ").lower()
            if choice != 'y':
                print("爬取终止！")
                break
                
            current_url = next_url

        except Exception as e:
            print(f"发生错误：{str(e)}")
            break

if __name__ == "__main__":
    target_url = "https://www.35wx.la/9_9319/5369434.html"
    crawl_novel(target_url)
    print("内容已保存到 novel_content.txt")