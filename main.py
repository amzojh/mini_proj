import os
import argparse

import FinanceDataReader as fdr
import pandas as pd

from Database.dbconnector import sqlConnector
from Database.querymaker import queryMaker
from Util.loggerutil import defaultLogger
from Crawling.companylist import companyListCrwaler
from Crawling.dart import dartCrawler

working_dir = os.getcwd()

if __name__ == "__main__":

    # sql_connector = sqlConnector()
    logger_class = defaultLogger()
    company_list_crawler = companyListCrwaler(logger_class, working_dir)
    company_df = company_list_crawler.get_listing_company()

    dart_crawler_instance = dartCrawler(logger_class, working_dir)
    dart_crawler_instance.get_report_type()
    dart_crawler_instance.get_all_report_list(company_df)
    # query_maker_instance = queryMaker()