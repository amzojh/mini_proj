from Crawling.base import baseCrwaler
from bs4 import BeautifulSoup as bs
import pandas as pd
import 

class stockPrice(baseCrwaler):
    def __init__(self, logger_class):
        super().__init__(logger_class)

    def process(self, company_list, date_from, date_to):
        pass