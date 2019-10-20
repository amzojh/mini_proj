import os
import sys
import argparse
import glob

import FinanceDataReader as fdr
import pandas as pd



import asyncio

from Util.loggerutil import defaultLogger
from Util.asyncioutil import asynciUtil
from Util.seleniumutil import seleniumUtil
from Util.excelutil import excelUtil

from Database.dbconnector import sqlConnector
from Database.querymaker import queryMaker
from Crawling.companylist import companyListCrwaler
from Crawling.dart import dartCrawler

from Database import db_session
from Database.Model.dart import baseAbstract

working_dir = os.getcwd()

if __name__ == "__main__":


    excel_util_instance = excelUtil()
    excel_util_instance.remove_all_xlsx_files_name_ranges("")

"""

    print(sys.path)

    print(baseAbstract.__dict__)

    # sql_connector = sqlConnector()
    logger_class = defaultLogger()
    # company_list_crawler = companyListCrwaler(logger_class, working_dir)
    # company_df = company_list_crawler.get_listing_company()

    dart_crawler_instance = dartCrawler(logger_class, working_dir)
    # df_dart_report_type = dart_crawler_instance.get_report_type()
    query_maker_instance = queryMaker(db_session)

    excel_list = glob.glob("C:/DART/새 폴더/*.xlsx")

    for excel_path in excel_list:
        df = pd.read_excel(excel_path, index_col=0)
        insert_query_statement = query_maker_instance.insert_query_from_df(df, table_name="DartCompanyList")
        db_session.execute(insert_query_statement)

    # loop = asyncio.get_event_loop()
    # async_util_instance = asynciUtil(logger_class, loop)
    # loop.run_until_complete(dart_crawler_instance.get_all_dart_company_list(async_util_instance))
"""