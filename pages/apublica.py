import requests
from bs4 import BeautifulSoup
from pages.news import News


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
            news_object = {
                    'title': result.find('h4', class_='card-title mb-2').text,
                    'link': result.find('a')['href'],
                    'content': result.find('p', class_='card-text summary d-none d-sm-block').text,
                    'date': result.find('span', class_='card-date').text
                }

            self.news.append(
                News(**self.remove_breakline_from_dict(news_object))
            )

    def remove_breakline_from_dict(self, dictionary):
        for key in dictionary:
            dictionary[key] = dictionary[key].replace('\n', '').replace('  ', '')
        return dictionary
