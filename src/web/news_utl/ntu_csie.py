import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_ntu_csie_news():
    URL = 'https://www.csie.ntu.edu.tw/'

    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')

    news = soup.find_all('div', class_='w-annc')[0]

    news_df = pd.DataFrame(columns=['title', 'date', 'link'])
    #full_link = f"https://www.csie.ncku.edu.tw{link}"
    dates = news.find_all('span', class_='w-annc__postdate')
    news_items = news.find_all('a')
    for n, d in zip(news_items, dates):
        title = n.text
        date = d.text
        link = n['href']
        news_df = news_df._append({'title': title, 'date': date, 'link': f"https://www.csie.ntu.edu.tw{link}"}, ignore_index=True)

    return news_df

if __name__ == '__main__':
    news_df = fetch_ntu_csie_news()
    print(news_df)
    news_df.to_csv('news.csv', index=False)