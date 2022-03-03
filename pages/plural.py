import requests
from bs4 import BeautifulSoup
from pages.news import News
from tools import utils

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class PluralNews:
    title = 'Plural'
    base_url = 'https://www.plural.jor.br/'

    def __init__(self, keyword):
        self.url = self.base_url + '?s=' + keyword
        self.news = list()

    def crawl(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='caption')
        for result in results:
            try:
                news_link = result.find('h1').find('a')['href']
                news_content = requests.get(news_link)

                soup = BeautifulSoup(news_content.text, 'html.parser')
                date = soup.find('div', class_='data-hora').text
                news_object = utils.remove_breakline_from_dict({
                    'title': result.find('h1').find('a')['title'],
                    'link': news_link,
                    'content': result.find('p').text,
                    'date': date
                })
                try:
                    news_object['date'] = utils.format_date(
                        news_object['date'].split(' -')[0],
                        date_format_from='%d %b %Y'
                    )
                except ValueError:
                    news_object['date'] = utils.format_date(
                        news_object['date'].split(' -')[0],
                        date_format_from='%d %B %Y'
                    )
                self.news.append(News(**news_object))
            except requests.exceptions.ConnectionError:
                print('ConnectionError')
                continue
