import requests
from bs4 import BeautifulSoup

URL = 'https://www.csie.ntu.edu.tw/'

r = requests.get(URL)
soup = BeautifulSoup(r.text, 'html.parser')

news = soup.find_all('div', class_='w-annc')

print(news[0].text)