import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_content(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
        return None

def parse_chapter(html):
    soup = BeautifulSoup(html, 'html.parser')
    content_div = soup.find('div', id='content')
    chapter_info = soup.find('div', class_='bookname').find('h1').text.strip()
    
    # Extracting chapter number and title
    section, title = chapter_info.split(' ', 1)
    section_number = section[:-1]  # Remove the '节' character
    
    # Check if it's the last page of the chapter
    parts = title.split('(')
    is_last_page = parts[-1].startswith('b/')
    
    # Clean up the text content
    paragraphs = [p for p in content_div.stripped_strings if "最新网址：www.35wx.la" not in p]
    clean_text = '\n'.join(paragraphs[1:-1])  # Exclude first and last lines with website info
    
    return section_number, title, clean_text, is_last_page

def get_next_link(html, is_last_page):
    soup = BeautifulSoup(html, 'html.parser')
    if is_last_page:
        next_tag = "下一章"
    else:
        next_tag = "下一页"
    next_link = soup.find('a', text=next_tag)
    if next_link:
        return next_link['href']
    return None

def save_to_file(filename, section_title, content):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f'\r\n{section_title}\r\n')
        file.write(content + '\r\n')

def main():
    base_url = 'https://www.35wx.la'
    start_url = 'https://www.35wx.la/9_9319/5369434.html'
    filename = 'novel.txt'
    
    while start_url:
        html = fetch_content(start_url)
        if html:
            section_number, title, content, is_last_page = parse_chapter(html)
            section_title = f'第{section_number}节 {title.split("(", 1)[0]}'
            save_to_file(filename, section_title, content)
            
            next_url = get_next_link(html, is_last_page)
            if next_url:
                start_url = urljoin(base_url, next_url) if not next_url.startswith('http') else next_url
                user_input = input("是否转到下一页(yes/no)? ")
                if user_input.lower() != 'yes':
                    break
            else:
                break
        else:
            break

if __name__ == '__main__':
    main()