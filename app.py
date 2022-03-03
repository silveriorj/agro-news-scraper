from json.tool import main
from pages.apublica import APublicaNews
from pages.diplomatique import DiplomatiqueNews
from pages.joioetrigo import JoioetrigoNews
from pages.jornalistaslivres import JornalistasLivresNews
from pages.plural import PluralNews
from pages.reporterbrasil import ReporterBrasilNews
from pages.ruralistas import RuralistasNews
from pages.terrasemmales import TerraSemMalesNews

import pandas as pd
import logging
import argparse

news_websites = [
    APublicaNews, DiplomatiqueNews, JoioetrigoNews,
    JornalistasLivresNews, PluralNews,
    ReporterBrasilNews, RuralistasNews, TerraSemMalesNews
]

def start_crawler(topic):
    news = []
    for site in news_websites:
        try:
            logging.info(f'Starting {site.__name__}')
            print(f'Starting {site.__name__}')
            info_site = site(topic)
            info_site.crawl()
            news += info_site.news
        except Exception as e:
            logging.error(f'Error in {site.__name__}')
            print(f'Error in {site.__name__}')
            print(e)

    json_news = [news_object.dict() for news_object in news]
    df_news = pd.DataFrame(json_news)
    df_news.to_csv(f'news_{topic}.csv', index=False)
    df_news.to_excel(f'news_{topic}.xlsx', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A test program.')

    parser.add_argument(
        "-t", "--topic",
        help="Add a topic to search for",
        action="store"
    )
    args = parser.parse_args()
    start_crawler(args.topic)