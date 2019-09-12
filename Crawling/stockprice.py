from Crawling.base import baseCrwaler
from bs4 import BeautifulSoup as bs
import pandas as pd
import 

class stockPrice(baseCrwaler):
    def __init__(self, logger_class, base_path=None):
        super().__init__(logger_class, base_path)

    def process(self, company_list, date_from, date_to):
        pass