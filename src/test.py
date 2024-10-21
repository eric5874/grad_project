import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = 'https://www.csie.ntu.edu.tw/'

r = requests.get(URL)
soup = BeautifulSoup(r.text, 'html.parser')

news = soup.find_all('div', class_='w-annc')[0]

# print(news[0].text)

news_df = pd.DataFrame(columns=['title', 'date', 'link'])
# 

# save to html
with open('news.html', 'w', encoding='utf-8') as f:
    f.write(str(news))

# <span class="w-annc__postdate"> 2024-10-01</span>
dates = news.find_all('span', class_='w-annc__postdate')
news = news.find_all('a')
for n, d in zip(news, dates):
    title = n.text
    date = d.text
    link = n['href']
    news_df = news_df._append({'title': title, 'date': date, 'link': link}, ignore_index=True)

news_df.to_csv('news.csv', index=False)