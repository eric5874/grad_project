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
    url = "https://www.csie.ntu.edu.tw/zh_tw/more_announcement/114%E5%AD%B8%E5%B9%B4%E5%BA%A6%E7%A2%A9%E5%8D%9A%E5%A3%AB%E7%8F%AD%E7%94%84%E8%A9%A6%E6%AD%A3%E5%82%99%E5%8F%96%E5%90%8D%E5%96%AE-%E5%90%AB%E9%80%95%E5%8D%9A-57212853"
    print(read_news_content(url))