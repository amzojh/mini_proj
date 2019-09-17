import os

from Crawling.base import baseCrwaler
from bs4 import BeautifulSoup as bs
import pandas as pd
import FinanceDataReader as fdr


class companyListCrwaler(baseCrwaler):
    def __init__(self, logger_class, base_path=None):
        super().__init__(logger_class, base_path)
        self.listing_company_path = os.path.join(self.base_path, "/listing/KRX_listing.csv")


    def _fdr_get_listing_company(self, market):
        return fdr.StockListing(market)

    def get_listing_company(self):

        # market_list = ["KOSPI", "KOSDAQ", "KONEX", "NASDAQ", "NYSE", "AMEX", "SP500"]
        market_list = ["KOSPI", "KOSDAQ", "KONEX"]

        df_list = []
        for market in market_list:
            df = self._fdr_get_listing_company(market)
            df["market"] = market
            df = df.apply(lambda x: x.astype(str), axis=1)
            
            if market in ["KOSPI", "KOSDAQ", "KONEX"]:
                df["symbol"] = df["symbol"].str.zfill(6)


            df.columns = ["symbol","company_name","sector","industry","market"]
            df_list.append(df)

        df = pd.concat(df_list)

        if not os.path.exists("/listing"):
            os.makedirs("/listing")

        print(df.head(10))
        df.to_csv("/listing/KRX_listing.csv")

        return df

    def process(self):
        page_index = 1


        company_detail_list = []
        for page_index in range(1, 25):
            url = f"""
                https://dev-kind.krx.co.kr/corpgeneral/corpList.do?method=searchCorpList&pageIndex={str(page_index)}&currentPageSize=100&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=13&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all
                """
            res = self.webutil.no_exception_get(url)
            bs_obj = bs(res.text, 'lxml')
            table_obj = bs_obj.select_one("table[class='list type-00 tmt30'][summary]")            
            tr_tags = table_obj.select("tbody tr")

            for tr_tag in tr_tags:
                company_detail = {}
                td_tags = tr_tag.select("td")
                company_detail["Type"] = str.strip(td_tags[0].img["alt"])
                company_detail["CompanyName"] = str.strip(td_tags[0].a.text)
                company_detail["ServiceType"] = str.strip(td_tags[1].text)
                company_detail["ServiceTypeDetail"] = str.strip(td_tags[2].text)
                company_detail["ListDate"] = str.strip(td_tags[3].text)
                company_detail["FiscalMonth"] = str.strip(td_tags[4].text)
                company_detail["CEO"] = str.strip(td_tags[5]["title"]) 
                company_detail["Location"] = str.strip(td_tags[7].text) 
                company_detail_list.append(company_detail)

        df_1 = pd.DataFrame.from_records(company_detail_list)
        df_1 = df_1.set_index(df_1["CompanyName"])
        url = "https://dev-kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=13&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all"
        df_2 = pd.read_html(io=url, index_col=0)[0]["종목코드"].astype(str).str.strip()
        df_2.name = "CompanyCode"
        df_1 = pd.concat([df_1, df_2], join='inner', axis=1)
        df_1.to_csv("companyList.csv")