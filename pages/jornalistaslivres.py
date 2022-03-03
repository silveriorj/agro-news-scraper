import requests
from bs4 import BeautifulSoup
from pages.news import News
from tools import utils

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class JornalistasLivresNews:
    title = 'JornalistasLivres'
    base_url = 'https://jornalistaslivres.org/'

    def __init__(self, keyword):
        self.url = self.base_url + '?s=' + keyword
        self.news = list()

    def crawl(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('article')
        for result in results:
            news_object = utils.remove_breakline_from_dict({
                'title': result.find(
                    'h3', class_='elementor-post__title'
                ).text,
                'link': result.find(
                    'a', class_='elementor-post__thumbnail__link'
                )['href'],
                'content': result.find(
                    'div', class_='elementor-post__excerpt'
                ).text,
                'date': result.find(
                    'span', class_='elementor-post-date'
                ).text
            })
            news_object['date'] = utils.format_date(
                news_object['date'],
                date_format_from='%d/%m/%y'
            )
            self.news.append(News(**news_object))
