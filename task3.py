import requests
from bs4 import BeautifulSoup
import re

KEYWORDS = ['дизайн', 'фото', 'web', 'python','Гаджеты', 'RT', 'Nvidia']

response = requests.get('https://habr.com/ru/all/')
if not response.ok:
    raise Exception('Error')

text = response.text

soup = BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article')

atcl = []
hubs = []
body = []

for article in articles:
    previews = article.find_all(class_='tm-article-snippet__title-link')
    hubs = article.find_all(class_='tm-article-snippet__hubs-item-link')
    body = article.find_all(class_='article-formatted-body article-formatted-body_version-2')
    atcl = [a.text.strip() for a in previews]
    hubs = [span.text.strip() for span in hubs]
    atcl.extend(hubs)
    body = [div.text.strip() for div in body]
    atcl.extend(body)

    joined_line = ','.join(atcl)
    a_pat = '(?:{})'.format('|'.join(KEYWORDS))
    match = re.search(a_pat, joined_line)
    if match:
        link = 'https://habr.com' + (article.find('h2').find('a').attrs.get('href'))
        date = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs.get('datetime')
        print(f'<{date}> - <{atcl[0]}> - <{link}>')