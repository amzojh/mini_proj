import os
import argparse

from Database.dbconnector import sqlConnector
from Util.loggerutil import defaultLogger
from Crawling.companylist import companyListCrwaler

if __name__ == "__main__":
    sql_connector = sqlConnector()
    logger_class = defaultLogger()
    company_list_crwaler = companyListCrwaler(logger_class)    
    company_list_crwaler.process()

    print(sql_connector)