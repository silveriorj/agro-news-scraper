import requests
from bs4 import BeautifulSoup
from pages.news import News
from datetime import datetime
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
            news_object = self.remove_breakline_from_dict({
                'title': result.find('h3', class_='elementor-post__title').text,
                'link': result.find('a', class_='elementor-post__thumbnail__link')['href'],
                'content': result.find('div', class_='elementor-post__excerpt').text,
                'date': result.find('span', class_='elementor-post-date').text
            })
            news_object['date'] = self.format_date(news_object['date'])

            self.news.append(
                News(**news_object)
            )

    def remove_breakline_from_dict(self, dictionary):
        for key in dictionary:
            dictionary[key] = dictionary[key].replace('\n', '').replace('  ', '')
        return dictionary

    def format_date(self, date):
        date = datetime.strptime(date.capitalize().strip(), '%d/%m/%y')
        return date.strftime('%d/%m/%Y')
