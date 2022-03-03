import requests
from bs4 import BeautifulSoup
from pages.news import News
from datetime import datetime
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
                news_object = self.remove_breakline_from_dict({
                    'title': result.find('h1').find('a')['title'],
                    'link': news_link,
                    'content': result.find('p').text,
                    'date': date
                })
                news_object['date'] = self.format_date(news_object['date'])

                self.news.append(
                    News(**news_object)
                )
            except requests.exceptions.ConnectionError:
                print('ConnectionError')
                continue

    def remove_breakline_from_dict(self, dictionary):
        for key in dictionary:
            dictionary[key] = dictionary[key].replace('\n', '').replace('  ', '')
        return dictionary

    def format_date(self, date):
        date = date.split(' -')[0]
        date = datetime.strptime(date.capitalize(), '%d %b %Y')
        return date.strftime('%d/%m/%Y')
