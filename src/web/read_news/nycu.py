import requests
from bs4 import BeautifulSoup

def read_news_content(url: str) -> str:
    if url[-3:] == "pdf":
        return "This is a PDF file, please download and view it. Link: " + url
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('div', class_='s-annc__post-body').text
    return content

if __name__ == "__main__":
    url = "https://newstudents.nycu.edu.tw/wp-content/uploads/2018/08/113A%E7%A0%94%E7%A9%B6%E6%89%80%E6%96%B0%E7%94%9F%E5%85%A5%E5%AD%B8%E9%A0%88%E7%9F%A520240624.pdf"
    print(read_news_content(url))