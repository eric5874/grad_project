import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd

def fetch_ncu_news():
    URL = 'https://pdc.adm.ncu.edu.tw/'
    ua = UserAgent(browsers=['safari'])

    # 發送請求
    r = requests.get(URL, headers={'User-Agent': ua.random})

    # 使用 chardet 檢測編碼
    try:
        import chardet
        detected_encoding = chardet.detect(r.content)['encoding']
    except ImportError:
        detected_encoding = None
    
    if detected_encoding:
        r.encoding = detected_encoding
    else:
        r.encoding = 'big5'  # 嘗試設為 Big5

    soup = BeautifulSoup(r.text, 'html.parser')

    # 找到包含新聞的區塊
    news_items = soup.find_all('div', style="padding-top:20px;padding-left:20px;")
    news_df = pd.DataFrame(columns=['date', 'unit', 'title', 'link'])

    for item in news_items:
        date = item.find('small').text.strip()
        unit = item.find_all('small')[1].text.strip()
        title = item.find('a').text.strip()
        link = item.find('a')['href']
        if not link.startswith('http'):
            link = f"https://pdc.adm.ncu.edu.tw{link}"
        news_df = news_df._append({'date': date, 'unit': unit, 'title': title, 'link': link}, ignore_index=True)

    return news_df

if __name__ == '__main__':
    news_df = fetch_ncu_news()
    print(news_df)
    news_df.to_csv('ncu_news.csv', index=False, encoding='utf-8-sig')
