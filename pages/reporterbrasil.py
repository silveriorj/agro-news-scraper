import requests
from bs4 import BeautifulSoup
from pages.news import News
from tools import utils

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class ReporterBrasilNews:
    title = 'ReporterBrasil'
    base_url = 'https://reporterbrasil.org.br/busca/'

    def __init__(self, keyword):
        self.url = self.base_url + '?search_query=' + keyword
        self.news = list()

    def crawl(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('article')
        for result in results:
            news_object = utils.remove_breakline_from_dict({
                'title': result.find('h2').text,
                'link': result.find('h2').find('a')['href'],
                'content': result.find('div', class_='metadata').text,
                'date': result.find('span', class_='date').text
            })
            news_object['date'] = utils.format_date(
                news_object['date'],
                date_format_from='%d/%m/%y'
            )
            self.news.append(News(**news_object))
