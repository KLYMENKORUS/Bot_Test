import random
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent


class GoogleRandomImage:
    """Парсинг рандомной картинки c Google"""

    def __init__(self, query: str):
        self.query = query
        self.url = f'https://www.google.com/search?q={self.query}&source=lnms&tbm=isch'
        self.browser = UserAgent()
        self.headers = {'user-agent': self.browser.google}

    def search(self):
        response = requests.get(url=self.url, headers=self.headers)
        try:
            soup = BS(response.content, 'lxml')
            images = soup.find_all('img')

            if len(images) > 0:
                return random.choice(images)['src']
            else:
                return None
        except:
            return None
