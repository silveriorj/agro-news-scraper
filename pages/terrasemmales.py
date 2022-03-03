import requests
from bs4 import BeautifulSoup
from pages.news import News
from tools import utils

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class TerraSemMalesNews:
    title = 'TerraSemMales'
    base_url = 'https://www.terrasemmales.com.br/'

    def __init__(self, keyword):
        self.url = self.base_url + '?s=' + keyword
        self.news = list()

    def crawl(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/50.0.2661.102 Safari/537.36',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('article')
        for result in results:
            content = result.find('div', class_='article-content clearfix')
            news_object = utils.remove_breakline_from_dict({
                'title': content.find('h2').find('a')['title'],
                'link': content.find('h2').find('a')['href'],
                'content': result.find(
                    'div',
                    class_='entry-content clearfix'
                ).text,
                'date': result.find('time', class_='entry-date').text
            })
            news_object['date'] = utils.format_date(
                news_object['date'],
                date_format_from='%d de %B de %Y'
            )
            self.news.append(News(**news_object))
