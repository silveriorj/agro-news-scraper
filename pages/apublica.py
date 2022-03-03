import requests
from bs4 import BeautifulSoup
from pages.news import News
from tools import utils

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class APublicaNews:
    title = 'APublica'
    base_url = 'https://apublica.org/'

    def __init__(self, keyword):
        self.url = self.base_url + '?s=' + keyword
        self.news = list()

    def crawl(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='row mb-5 brick-category-1')
        for result in results:
            news_object = utils.remove_breakline_from_dict({
                'title': result.find('h4', class_='card-title mb-2').text,
                'link': result.find('a')['href'],
                'content': result.find(
                    'p',
                    class_='card-text summary d-none d-sm-block'
                ).text,
                'date': self.format_date(result.find(
                    'span',
                    class_='card-date'
                ).text)
            })
            try:
                news_object['date'] = utils.format_date(
                    news_object['date'],
                    date_format_from='%d de %B de %Y'
                )
            except ValueError:
                news_object['date'] = utils.format_date(
                    news_object['date'],
                    date_format_from='%d/%m/%Y'
                )
            self.news.append(News(**news_object))
