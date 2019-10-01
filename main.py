import os
import sys
import argparse

import FinanceDataReader as fdr
import pandas as pd

import asyncio

from Util.loggerutil import defaultLogger
from Util.asyncioutil import asynciUtil
from Util.seleniumutil import seleniumUtil

from Database.dbconnector import sqlConnector
from Database.querymaker import queryMaker
from Crawling.companylist import companyListCrwaler
from Crawling.dart import dartCrawler

from Database import db_session
from Database.Model.dart import baseAbstract

working_dir = os.getcwd()

if __name__ == "__main__":
    print(sys.path)

    print(baseAbstract.__dict__)

    # sql_connector = sqlConnector()
    logger_class = defaultLogger()
    company_list_crawler = companyListCrwaler(logger_class, working_dir)
    company_df = company_list_crawler.get_listing_company()

    dart_crawler_instance = dartCrawler(logger_class, working_dir)
    df_dart_report_type = dart_crawler_instance.get_report_type()

    

    # loop = asyncio.get_event_loop()
    # async_util_instance = asynciUtil(logger_class, loop)
    # loop.run_until_complete(dart_crawler_instance.async_get_all_report_list(company_df, async_util_instance))