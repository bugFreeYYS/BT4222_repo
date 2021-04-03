import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import json
import datetime

def getArticleComplete(page_url):
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    articles = soup.find_all('div', {'class': 'article-module article'})
    return articles[0].text

def get_coindesk_data(num_pages=5):
    output = dict()
    for i in range(num_pages):
        print('Processing page {}'.format(i))
        request = requests.get('https://www.coindesk.com/wp-json/v1/search?keyword=bitcoin&page={}'.format(i))
        temp_data = json.loads(request.content)['results']
        for article in temp_data:
            print(article['url'])
            try:
                output[article['url']] = {
                    'tag': article['tag']['name'],
                    'title': article['title'],
                    'date': article['date'].split('T')[0],
                    'header': article['text'],
                    'complete_article': getArticleComplete(article['url'])
                }
                time.sleep(3)
            except:
                print("Error, sleep for 60s")
                time.sleep(60)
                try:
                    output[article['url']] = {
                        'tag': article['tag']['name'],
                        'title': article['title'],
                        'date': article['date'].split('T')[0],
                        'header': article['text'],
                        'complete_article': getArticleComplete(article['url'])
                    }
                except:
                    print("Error, sleep for 180s and skip this article")
                    time.sleep(180)
                    continue
    return pd.DataFrame.from_dict(output).transpose().sort_values('date')