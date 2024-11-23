import requests
from bs4 import BeautifulSoup

def read_news_content(url: str) -> str:
    if url[-3:] == "pdf":
        return "This is a PDF file, please download and view it. Link: " + url
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('span', class_='post-content').text
    return content

if __name__ == "__main__":
    url = "https://www.csie.ncku.edu.tw/zh-hant/news/12976"
    print(read_news_content(url))