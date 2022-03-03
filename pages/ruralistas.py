import requests
from bs4 import BeautifulSoup
from pages.news import News
from tools import utils

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class RuralistasNews:
    title = 'Ruralistas'
    base_url = 'https://deolhonosruralistas.com.br/'

    def __init__(self, keyword):
        self.url = self.base_url + '?s=' + keyword
        self.news = list()

    def crawl(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all(
            'div',
            class_='news_box_container news_box_first row'
        )
        for result in results:
            title = result.find('h3', class_='post_title title').text
            link = result.find('a', class_='news_box_link')['href']
            content = result.find('p', class_='news_box_desc').text

            news_content = requests.get(link)

            soup = BeautifulSoup(news_content.text, 'html.parser')
            date = soup.find('time', class_='entry-date').text

            news_object = utils.remove_breakline_from_dict({
                'title': title,
                'link': link,
                'content': content,
                'date': date
            })
            news_object['date'] = utils.format_date(
                news_object['date'],
                date_format_from='%d/%m/%Y'
            )
            self.news.append(News(**news_object))
