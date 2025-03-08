import os
import re
import time
import random
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import img2pdf
from PIL import Image

def get_base_url(url):
    """提取漫画基础URL"""
    match = re.match(r'^(https?://.*?/read-\d+)(?:-\d+)?/?$', url)
    return match.group(1) if match else url

def download_page(url, page_num, retries=5):
    """下载单个页面图片"""
    try:
        # 随机延迟（3-7秒）
        time.sleep(random.uniform(3, 7))
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': url
        }
        
        with requests.Session() as session:
            # 获取页面内容
            response = session.get(url, headers=headers)
            response.raise_for_status()
            
            # 解析页面内容
            soup = BeautifulSoup(response.text, 'html.parser')
            p_tag = soup.find('p', class_='font-2 text-dark text-center mb-3')
            
            if not p_tag:
                raise ValueError("未找到页码标签")
            
            # 获取图片标签
            img_tag = p_tag.find_next('img')
            if not img_tag or 'src' not in img_tag.attrs:
                raise ValueError("未找到有效图片标签")
            
            # 下载图片
            img_url = img_tag['src']
            img_response = session.get(img_url, headers=headers)
            img_response.raise_for_status()
            
            # 保存图片
            filename = f"comic_images/{page_num:03d}.webp"
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            
            print(f"✅ 成功下载第 {page_num} 页")
            return True
            
    except Exception as e:
        if retries > 0:
            print(f"⚠️ 重试第 {page_num} 页，剩余重试次数：{retries}，错误：{str(e)}")
            return download_page(url, page_num, retries-1)
        else:
            print(f"❌ 第 {page_num} 页下载失败，错误：{str(e)}")
            return False

def download_comic(initial_url, thread_num=5):
    """下载漫画主函数"""
    # 创建存储目录
    os.makedirs('comic_images', exist_ok=True)
    
    # 获取基础URL
    base_url = get_base_url(initial_url)
    
    # 初始化请求获取总页数
    with requests.Session() as session:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': initial_url
        }
        response = session.get(initial_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 解析页码信息
        p_tag = soup.find('p', class_='font-2 text-dark text-center mb-3')
        if not p_tag:
            raise ValueError("无法定位页码信息")
        
        page_info = p_tag.b.text.strip().split('(')[-1].rstrip(')')
        current_page, total_pages = map(int, page_info.split('/'))
        
        # 获取漫画名称
        img_tag = p_tag.find_next('img')
        comic_name = img_tag['alt'].strip() if img_tag else "未知漫画"
    
    # 生成所有页面URL
    urls = [(base_url if page == 1 else f"{base_url}-{page}", page) 
            for page in range(current_page, total_pages + 1)]
    
    print(f"📚 开始下载《{comic_name}》，共 {total_pages} 页")
    
    # 创建线程池下载
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_num) as executor:
        futures = [executor.submit(download_page, url, page) for url, page in urls]
        
        # 显示进度
        for future in concurrent.futures.as_completed(futures):
            future.result()  # 保持异常传播
    
    print("🎉 所有页面下载完成")
    return comic_name

def convert_to_pdf(comic_name):
    """转换为PDF文件"""
    try:
        # 获取排序后的图片列表
        images = sorted([f for f in os.listdir('comic_images') if f.endswith('.webp')],
                       key=lambda x: int(x.split('.')[0]))
        
        # 转换PDF
        with open(f"{comic_name}.pdf", "wb") as f:
            img_list = [Image.open(os.path.join('comic_images', img)) for img in images]
            pdf_bytes = img2pdf.convert([img.filename for img in img_list])
            f.write(pdf_bytes)
        
        print(f"✅ 成功生成PDF文件：{comic_name}.pdf")
        
    except Exception as e:
        print(f"❌ PDF转换失败：{str(e)}")

if __name__ == "__main__":
    # 配置参数
    initial_url = "https://issmh.cc/read-3456"
    thread_num = 5  # 可调节线程数
    
    try:
        # 下载漫画
        comic_name = download_comic(initial_url, thread_num)
        
        # 转换PDF
        if comic_name:
            convert_to_pdf(comic_name)
        
        # 清理临时文件（可选）
        import shutil
        shutil.rmtree('comic_images')
        
    except Exception as e:
        print(f"❌ 程序运行出错：{str(e)}")