import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import img2pdf
from PIL import Image
import time

def download_comic(initial_url):
    # 创建存储目录
    if not os.path.exists('comic_images'):
        os.makedirs('comic_images')
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': initial_url
    }
    
    current_url = initial_url
    comic_name = None
    page_count = 1
    total_pages = None
    session = requests.Session()
    
    while True:
        # 获取页面内容
        response = session.get(current_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 定位关键元素
        p_tag = soup.find('p', class_='font-2 text-dark text-center mb-3')
        if not p_tag:
            break
            
        # 解析页码信息
        page_info = p_tag.b.text.strip().split('(')[-1].rstrip(')')
        current_page, total_pages = map(int, page_info.split('/'))
        
        # 获取漫画名称（仅首次获取）
        img_tag = p_tag.find_next('img')
        if not comic_name:
            comic_name = img_tag['alt'].strip()
        
        # 下载图片
        img_url = img_tag['src']
        img_data = session.get(img_url, headers=headers).content
        
        # 保存图片
        filename = f"comic_images/{page_count:03d}.webp"
        with open(filename, 'wb') as f:
            f.write(img_data)
        print(f"已下载第 {page_count} 页")
        
        # 检查是否最后一页
        if current_page == total_pages:
            break
            
        # 获取下一页链接
        next_page_tag = p_tag.find_next('a')
        current_url = urljoin(current_url, next_page_tag['href'])
        page_count += 1
        
        # 防止请求过快的延迟
        time.sleep(1)
    
    return comic_name

def convert_to_pdf(comic_name):
    # 获取所有图片文件并按顺序排序
    images = sorted([f for f in os.listdir('comic_images') if f.endswith('.webp')])
    
    # 转换并保存为PDF
    with open(f"{comic_name}.pdf", "wb") as f:
        img_list = [Image.open(os.path.join('comic_images', img)) for img in images]
        pdf_bytes = img2pdf.convert([img.filename for img in img_list])
        f.write(pdf_bytes)
    
    print(f"已生成PDF文件：{comic_name}.pdf")

if __name__ == "__main__":
    initial_url = "https://issmh.cc/read-5588"
    
    # 下载漫画图片
    comic_name = download_comic(initial_url)
    
    # 转换为PDF
    if comic_name:
        convert_to_pdf(comic_name)
    else:
        print("未找到漫画名称，转换失败")