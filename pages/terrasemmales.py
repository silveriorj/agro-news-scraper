import requests
from bs4 import BeautifulSoup
from pages.news import News
from datetime import datetime
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
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('article')
        for result in results:
            content = result.find('div', class_='article-content clearfix')
            news_object = self.remove_breakline_from_dict({
                'title': content.find('h2').find('a')['title'],
                'link': content.find('h2').find('a')['href'],
                'content': result.find('div', class_='entry-content clearfix').text,
                'date': result.find('time', class_='entry-date').text
            })
            news_object['date'] = self.format_date(news_object['date'])
            self.news.append(News(**news_object))

    def remove_breakline_from_dict(self, dictionary):
        for key in dictionary:
            dictionary[key] = dictionary[key].replace('\n', '').replace('  ', '')
        return dictionary

    def format_date(self, date):
        date = datetime.strptime(date.capitalize(), '%d de %B de %Y')
        return date.strftime('%d/%m/%Y')
