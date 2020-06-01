from parsing_base import Parser
from bs4 import BeautifulSoup
import time


class OnlinerSellerParser(Parser):
    BASE_URL = 'https://{}.shop.onliner.by/'
    RANGE_SELLERS_ID = range(50000)

    def __init__(self):
        super().__init__()
        self.sellers = []

    def update_sellers(self):
        urls = [self.BASE_URL.format(seller_id) for seller_id in self.RANGE_SELLERS_ID]
        splited_urls = self.split_list(urls, 122)
        splited_ids = self.split_list(self.RANGE_SELLERS_ID, 122)
        print(splited_urls[17][21])
        print(splited_ids[17][21])
        for url_list in splited_urls:
            start_time = time.time()
            resps = self.requests.get(url_list)
            print(time.time() - start_time)
            for resp in resps:
                if self.is_seller_exists(resp):
                    print('oooooooo')


    @staticmethod
    def is_seller_exists(resp_text):
        soup = BeautifulSoup(resp_text, 'lxml')
        if soup.select_one('onliner-content'):
            return True


class Seller:
    def __init__(self, id):
        self.id = id
        self.url = f'https://{self.id}.shop.onliner.by/'
        self.name = str()
        self.activity = bool()
        self.phones = list()
        self.emails = list()




if __name__ == '__main__':
    parser = OnlinerSellerParser()
    parser.update_sellers()
