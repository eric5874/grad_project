import requests
from bs4 import BeautifulSoup

def read_news_content(url: str) -> str:
    if url[-3:] == "pdf":
        return "This is a PDF file, please download and view it. Link: " + url
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content.decode(response.apparent_encoding), 'html.parser')
    content = soup.findAll('p')
    content = [c.text for c in content]
    content = ' '.join(content)
    return content

if __name__ == "__main__":
    url = "https://pdc.adm.ncu.edu.tw/news_detail.asp?no=5056"
    print(read_news_content(url))