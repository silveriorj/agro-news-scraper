import requests
from bs4 import BeautifulSoup
from pages.news import News
from tools import utils

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class JoioetrigoNews:
    title = 'Joioetrigo'
    base_url = 'https://ojoioeotrigo.com.br/'

    def __init__(self, keyword):
        self.url = self.base_url + '?s=' + keyword
        self.news = list()

    def crawl(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='ht-post-wrapper')
        for result in results:
            news_object = utils.remove_breakline_from_dict({
                'title': result.find('h3', class_='entry-title').text,
                'link': result.find('a')['href'],
                'content': result.find('span', class_='excerpt_part').text,
                'date': result.find('span', class_='entry-date').text
            })
            news_object['date'] = utils.format_date(
                news_object['date'],
                date_format_from='%d.%m.%y'
            )
            self.news.append(News(**news_object))
