import os
import argparse

import FinanceDataReader as fdr
import pandas as pd

from Database.dbconnector import sqlConnector
from Database.querymaker import queryMaker
from Util.loggerutil import defaultLogger
from Crawling.companylist import companyListCrwaler



if __name__ == "__main__":

    os.chdir(os.getcwd())

    sql_connector = sqlConnector()
    logger_class = defaultLogger()
    query_maker_instance = queryMaker()
    company_list_crawler = companyListCrwaler(logger_class)


    market_list = ["KOSPI", "KOSDAQ", "KONEX", "NASDAQ", "NYSE", "AMEX", "SP500"]
    df_list = []
    for market in market_list:
        df = company_list_crawler.get_listing_company(market)
        df["Market"] = market
        df = df.apply(lambda x: x.astype(str), axis=1)
        
        if market in ["KOSPI", "KOSDAQ", "KONEX"]:
            df["Symbol"] = df["Symbol"].str.zfill(6)
        
        df_list.append(df)

    df = pd.concat(df_list)

    if not os.path.exists("/listing"):
        os.makedirs("/listing")

    print(df.head(10))
    df.to_csv("/listing/KRX_listing.csv")

    