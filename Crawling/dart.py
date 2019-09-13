import os
import datetime
import re

import numpy as np
from Crawling.base import baseCrwaler
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

class dartCrawler(baseCrwaler):
    def __init__(self, logger_class, base_path=None):
        super().__init__(logger_class, base_path)
        self.report_type_path = os.path.join(self.base_path, "/dart/reportType.csv")
        self.report_list_path = os.path.join(self.base_path, "/dart/reportList.csv")

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
        pass

    def _df_string_parsing(self, df):
        values = df.values.astype(str)
        values = np.char.strip(values)
        values = np.char.replace(values, "\t", "")
        values = np.char.replace(values, "\b", "")
        values = np.char.replace(values, "\n", "")
        df.iloc[:] = values

        return df


    def _parsing_search_table(self, bs_obj, doc_type):
        tr_obj_list = bs_obj.select("div.table_list>table[summary]>tbody>tr")
        report_list = []
        for tr_obj in tr_obj_list:
            report_dict = {}
            td_list = tr_obj.select('td')
            disclosure_company_info_tag = td_list[1].select_one('a[href]')
            report_info_tag = td_list[2].select_one('a[href]')
            issue_company_info_tag = td_list[3].select_one('div')
            date_info_tag = td_list[4]

            report_dict["TargetDisclosureCompany"] = str.strip(disclosure_company_info_tag.text)
            href = str(report_info_tag.attrs["href"])
            rcp_pattern = re.compile(r"rcpNo=(\d+)")
            rcp_id = re.search(rcp_pattern, href).group(1)
            
            report_dict["ReportLink"] = f"http://dart.fss.or.kr{href}"
            report_dict["ReportName"] = str.strip(report_info_tag.text)

            report_dict["IssueCompany"] = str.strip(issue_company_info_tag.text)
            report_dict["IssueDate"] = str(date_info_tag.text)
            report_dict["DocType"] = doc_type
            report_dict["rcpNo"] = rcp_id
            report_list.append(report_dict)

        return report_list


    def get_all_report_list(self, company_df, start_date="19990101", end_date=None):

        if end_date is None:
            today = datetime.datetime.today()
            end_date = f"{str(today.year)}{str(today.month).zfill(2)}{str(today.day).zfill(2)}"
        
        symbol_list = company_df["Symbol"].tolist()
        report_type_df = pd.read_csv(self.report_type_path)
        DocCode_list = report_type_df["DocCode"].tolist()

        for symbol in symbol_list:
            base_url = f"""
                http://dart.fss.or.kr/dsab001/search.ax
                """.replace("\n", "").replace(" ", "")
            session, res = self.webutil.no_exception_get(base_url,isReturnSession=True)

            company_report_list = []

            for doc_code in DocCode_list:
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
                data["publicType"] = str(doc_code)

                session, res = self.webutil.no_exception_post(base_url, session=session,cookies=cookies, isReturnSession=True, headers=headers, data=data)
                bs_obj = bs(res.text, 'lxml')
                count_bs_obj = bs_obj.select_one("div.page_list>p.page_info")

                if count_bs_obj is None:
                    continue

                text = str.strip(count_bs_obj.text)
                regex = re.compile(r"\[(\d+)/(\d+)\]")
                find_text = regex.search(text)
                for_loop_count = int(find_text.group(2))
                
                info_list = self._parsing_search_table(bs_obj, doc_code)
                for i in range(1, for_loop_count + 1):
                    cookies = session.cookies
                    data["currentPage"] = str(i)
                    session, res = self.webutil.no_exception_post(base_url, session=session,cookies=cookies, isReturnSession=True, headers=headers, data=data)
                    bs_obj = bs(res.text, 'lxml')
                    info_list = self._parsing_search_table(bs_obj, doc_code)
                    company_report_list = company_report_list + info_list

            df_company_report = pd.DataFrame(company_report_list)
            df_company_report = self._df_string_parsing(df_company_report)
            df_company_report["Symbol"] = symbol
            df_company_report.set_index(df_company_report["rcpNo"])

            if not os.path.exists(self.report_list_path):
                df_company_report.to_csv(self.report_list_path)


            df = pd.read_csv(self.report_list_path)
            

        #         headers = {}
        #         headers["currentPage"] = 1
                
        #         session, res = self.webutil.no_exception_get(base_url ,isReturnSession=True)
        #         bs_obj = bs(res.text, 'lxml')
        # # company_df["Symbol"].apply(lambda x: )
