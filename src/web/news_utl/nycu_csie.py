import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_nycu_admissions_info():
    # 這裡假設你抓取的 URL 是正確的頁面
    URL = 'https://www.cs.nycu.edu.tw/admission/graduate'  
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')

    # 定位到包含招生資訊的部分
    admissions_section = soup.find('strong').find_parent('h2').find_next('ul')

    # 創建 DataFrame
    admissions_df = pd.DataFrame(columns=['title', 'link'])

    # 提取所有的鏈接
    for li in admissions_section.find_all('li'):
        link_tag = li.find('a')
        if link_tag:
            title = link_tag.text.strip()  # 獲取鏈接的文本 (標題)
            link = link_tag['href']  # 獲取鏈接
            admissions_df = admissions_df._append({'title': title, 'link': link}, ignore_index=True)

    return admissions_df

if __name__ == '__main__':
    admissions_df = fetch_nycu_admissions_info()
    print(admissions_df)
    admissions_df.to_csv('nycu_admissions_info.csv', index=False)
