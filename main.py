from parsing_base import Parser
from bs4 import BeautifulSoup
import time


class OnlinerSellerParser(Parser):
    BASE_URL = 'https://{}.shop.onliner.by/'
    RANGE_SELLERS_ID = range(50000)
    SPLIT_RANGE = 500

    def __init__(self):
        super().__init__()
        self.sellers = []

    def update_sellers(self):
        self.sellers = []
        urls = [self.BASE_URL.format(seller_id) for seller_id in self.RANGE_SELLERS_ID]
        splited_urls = self.split_list(urls, self.SPLIT_RANGE)
        splited_ids = self.split_list(self.RANGE_SELLERS_ID, self.SPLIT_RANGE)
        for index_1 in range(len(splited_urls)):
            resps = self.requests.get(splited_urls[index_1])
            for index_2 in range(len(resps)):
                print(splited_urls[index_1][index_2])
                if self.is_seller_exists(resps[index_2]):
                    self.sellers.append(Seller(splited_ids[index_1][index_2], resps[index_2]))
        self.update_info_sellers()

    def update_info_sellers(self):
        for seller in self.sellers:
            seller.update_info()

    def save_sellers_excel(self):
        data = []
        for seller in self.sellers:
            data.append(seller.get_data())
        self.save_excel(data, 'data.xls')


    @staticmethod
    def is_seller_exists(resp_text):
        soup = BeautifulSoup(resp_text, 'lxml')
        if soup.select_one('.onliner-content'):
            return True


class Seller:
    def __init__(self, id, resp):
        self.id = id
        self.resp = resp
        self.url = f'https://{self.id}.shop.onliner.by/'
        self.name = str()
        self.activity = bool()
        self.phones = list()
        self.emails = list()

    def update_info(self):
        soup = BeautifulSoup(self.resp, 'lxml')
        self.name = soup.select_one('.sells-title').text
        if soup.select_one('.sells-shop-off'):
            self.activity = False
        else:
            self.activity = True
        self.phones = [phone_block.text.replace(u'\xa0', ' ').replace('\n', '') for phone_block in soup.select('.sells-contacts-list-itm._phone')]
        self.emails = [emails_block.text.replace('\n', '') for emails_block in soup.select('.sells-contacts-list-itm._mail')]

    def get_data(self):
        phones = '\n'.join(self.phones)
        emails = '\n'.join(self.emails)
        if self.activity:
            activity = 'да'
        else:
            activity = 'нет'
        return [self.url, self.name, activity, phones, emails]


if __name__ == '__main__':
    parser = OnlinerSellerParser()
    parser.update_sellers()
    parser.save_sellers_excel()
