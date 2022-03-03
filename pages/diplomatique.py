import requests
from bs4 import BeautifulSoup
from pages.news import News
from tools import utils

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class DiplomatiqueNews:
    title = 'Diplomatique'
    base_url = 'https://diplomatique.org.br/'

    def __init__(self, keyword):
        self.url = self.base_url + 'search/' + keyword
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
        results = soup.find_all('div', class_='relative w-100 px-3 px-sm-0')
        for result in results:
            title = result.find('h4').text
            link = result.find('a')['href']
            news_content = requests.get(link, headers=headers)

            soup = BeautifulSoup(news_content.text, 'html.parser')
            date = soup.find('div', class_='date').text

            content = result.find('div', class_='text-article').text
            content = content.replace('\n', ' ')
            news_object = utils.remove_breakline_from_dict({
                    'title': title,
                    'link': link,
                    'content': content,
                    'date': date
                })
            news_object['date'] = utils.format_date(
                news_object['date'],
                date_format_from='%d de %B de %Y'
            )
            self.news.append(News(**news_object))
