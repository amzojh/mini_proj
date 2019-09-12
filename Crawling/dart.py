import os
import datetime

from Crawling.base import baseCrwaler
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

class dartCrawler(baseCrwaler):
    def __init__(self, logger_class, base_path=None):
        super().__init__(logger_class, base_path)
        self.report_type_path = os.path.join(self.base_path, "/dart/reportType.csv")


    def get_report_type(self):
        url = "http://dart.fss.or.kr/"
        session, res = self.webutil.no_exception_get(url, isReturnSession=True)
        bs_obj = bs(res.text, 'lxml')
        bs_obj = bs_obj.select_one("div[id='main_layer_popup']")
        dl_list = bs_obj.select("dl[id^='divPublicType_']")

        mapping_list = []

        for dl_tag in dl_list:
            input_list = dl_tag.select("dd>input[type='checkbox']")
            for input_tag in input_list:
                input_dict = {}
                input_dict["DocCode"] = str(input_tag["value"])
                input_dict["DocDescription"] = str(input_tag["title"])
                mapping_list.append(input_dict)
                
        df = pd.DataFrame(mapping_list)

        if not os.path.exists("/dart"):
            os.makedirs("/dart")

        df.to_csv(self.report_type_path)

        return df

    def _header_setting(self):

    def get_all_report_list(self, company_df, start_date="19990101", end_date=None):

        if end_date is None:
            today = datetime.datetime.today()
            end_date = f"{str(today.year){str(today.month).zfill(2))}{str(today.day).zfill(2)}"
        
        symbol_list = company_df["Symbol"].tolist()
        report_type_df = pd.read_csv(self.report_type_path)
        DocCode_list = report_type_df["DocCode"].tolist()

        for symbol in symbol_list:
            base_url = f"""
                http://dart.fss.or.kr/dsab001/search.ax
                """.replace("\n", "").replace(" ", "")
            session, res = self.webutil.no_exception_get(base_url,isReturnSession=True)

            for DocCode in DocCode_list:
                session.headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36"
                cookies = session.cookies
                headers = {}
                headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36"
                headers["Origin"] = "http://dart.fss.or.kr"
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                headers["Host"] = "dart.fss.or.kr"

                data = {}
                data["currentPage"] = "1"
                data["maxResults"] = "100"
                data["maxLinks"] = "10"
                data["sort"] = "date"
                data["series"] = "desc"
                data["textCrpNm"] = str(symbol)
                data["startDate"] = start_date
                data["endDate"] = end_date
                data["publicType"] = str(DocCode)

                session, res = self.webutil.no_exception_post(base_url, session=session,cookies=cookies, isReturnSession=True, headers=headers, data=data)
                bs_obj = bs(res.text, 'lxml')
                bs_obj = bs_obj.select_one("div.page_list>p.page_info")
                print(bs_obj)
        #         headers = {}
        #         headers["currentPage"] = 1
                
        #         session, res = self.webutil.no_exception_get(base_url ,isReturnSession=True)
        #         bs_obj = bs(res.text, 'lxml')
        # # company_df["Symbol"].apply(lambda x: )
