import os
import datetime
import re
import asyncio

import numpy as np
from Crawling.base import baseCrwaler
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests


class dartOpenApi(baseCrwaler):

    def __init__(self, logger_class, base_path = None):

        super().__init__(logger_class, base_path)


    





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
                input_dict["document_code"] = str(input_tag["value"])
                input_dict["document_description"] = str(input_tag["title"])
                mapping_list.append(input_dict)
                
        df = pd.DataFrame(mapping_list)

        if not os.path.exists("/dart"):
            os.makedirs("/dart")

        df.to_csv(self.report_type_path)

        return df

    def _setting_header(self):
        headers = {}
        headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36"
        headers["Origin"] = "http://dart.fss.or.kr"
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Host"] = "dart.fss.or.kr"

        return headers
    
    def _setting_query_params(self, symbol, doc_code, start_date, end_date):
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

        return data


    def _parsing_df_string(self, df):
        values = df.values.astype(str)
        values = np.char.strip(values)
        values = np.char.replace(values, "\t", "")
        values = np.char.replace(values, "\b", "")
        values = np.char.replace(values, "\n", "")
        df.iloc[:] = values

        return df



    def _parsing_search_table(self, bs_obj, doc_type, symbol):
        tr_obj_list = bs_obj.select("div.table_list>table[summary]>tbody>tr")
        report_list = []
        for tr_obj in tr_obj_list:
            report_dict = {}
            td_list = tr_obj.select('td')
            disclosure_company_info_tag = td_list[1].select_one('a[href]')
            report_info_tag = td_list[2].select_one('a[href]')
            issue_company_info_tag = td_list[3].select_one('div')
            date_info_tag = td_list[4]

            href = str(report_info_tag.attrs["href"])
            rcp_pattern = re.compile(r"rcpNo=(\d+)")
            rcp_id = re.search(rcp_pattern, href).group(1)
            report_dict["disclosure_company"] = str.strip(disclosure_company_info_tag.text)
            report_dict["report_link"] = f"http://dart.fss.or.kr{href}"
            report_dict["report_name"] = str.strip(report_info_tag.text)

            report_dict["issue_company"] = str.strip(issue_company_info_tag.text)
            report_dict["issue_date"] = str(date_info_tag.text)
            report_dict["document_type"] = doc_type
            report_dict["report_id"] = rcp_id
            report_dict["symbol"] = symbol
            report_list.append(report_dict)

        return report_list

    def _get_symbol_list(self, company_df):
        download_symbol_list = []
        if os.path.exists(self.report_list_path):
            download_symbol_list = pd.read_csv(self.report_list_path, index_col=0)
            download_symbol_list = download_symbol_list["symbol"].drop_duplicates(keep='first').astype(str).str.zfill(6).tolist()
        
        objective_symbol_list = company_df["symbol"].astype(str).str.zfill(6).tolist()
        
        return list(set(objective_symbol_list) - set(download_symbol_list))

    def get_all_report_list(self, company_df, start_date="19990101", end_date=None):

        if end_date is None:
            today = datetime.datetime.today()
            end_date = f"{str(today.year)}{str(today.month).zfill(2)}{str(today.day).zfill(2)}"

        symbol_list = self._get_symbol_list(company_df)

        report_type_df = pd.read_csv(self.report_type_path, index_col=0)
        DocCode_list = report_type_df["document_code"].tolist()

        for symbol in symbol_list:
            base_url = f"""
                http://dart.fss.or.kr/dsab001/search.ax
                """.replace("\n", "").replace(" ", "")
            session, res = self.webutil.no_exception_get(base_url,isReturnSession=True)

            company_report_list = []

            for doc_code in DocCode_list:
                session.headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36"
                cookies = session.cookies
                headers = self._setting_header()

                data = self._setting_query_params(symbol, doc_code, start_date, end_date)

                session, res = self.webutil.no_exception_post(base_url, session=session,cookies=cookies, isReturnSession=True, headers=headers, data=data)
                bs_obj = bs(res.text, 'lxml')
                count_bs_obj = bs_obj.select_one("div.page_list>p.page_info")

                if count_bs_obj is None:
                    continue

                text = str.strip(count_bs_obj.text)
                regex = re.compile(r"\[(\d+)/(\d+)\]")
                find_text = regex.search(text)
                for_loop_count = int(find_text.group(2))
                info_list = self._parsing_search_table(bs_obj, doc_code, symbol)
                company_report_list = company_report_list + info_list 
                for i in range(2, for_loop_count + 1):
                    cookies = session.cookies
                    data["currentPage"] = str(i)
                    session, res = self.webutil.no_exception_post(base_url, session=session,cookies=cookies, isReturnSession=True, headers=headers, data=data)
                    bs_obj = bs(res.text, 'lxml')
                    info_list = self._parsing_search_table(bs_obj, doc_code, symbol)
                    company_report_list = company_report_list + info_list


            df = None
            if os.path.exists(self.report_list_path):
                df = pd.read_csv(self.report_list_path, index_col=0)

            df_company_report = pd.DataFrame(company_report_list)
            df_company_report = self._parsing_df_string(df_company_report)
            df_company_report.set_index(df_company_report["report_id"])
            df = pd.concat([df, df_company_report])
            df.drop_duplicates(["report_id"], inplace=True)
            df.to_csv(self.report_list_path)


    async def async_get_all_report_list(self, company_df, asyncio_util, start_date="19990101", end_date=None):

        if end_date is None:
            today = datetime.datetime.today()
            end_date = f"{str(today.year)}{str(today.month).zfill(2)}{str(today.day).zfill(2)}"
        symbol_list = self._get_symbol_list(company_df)
        report_type_df = pd.read_csv(self.report_type_path, index_col=0)
        DocCode_list = report_type_df["document_code"].tolist()

        for symbol in symbol_list:
            base_url = f"""
                http://dart.fss.or.kr/dsab001/search.ax
                """.replace("\n", "").replace(" ", "")
            session, res = self.webutil.no_exception_get(base_url,isReturnSession=True)
            cookies = session.cookies
            asyncio_util.make_client(cookies=cookies)
            task_list = []
            
            for doc_code in DocCode_list:
                headers = self._setting_header()
                data = self._setting_query_params(symbol, doc_code, start_date, end_date)
                task = asyncio.ensure_future(self.async_get_report_list(asyncio_util, base_url, headers, data, doc_code, symbol)) 
                task_list.append(task)
                
            return_list = await asyncio.gather(*task_list)
            await self.async_update_at_csv_file(return_list)
            await asyncio_util.client.close()

    async def async_update_at_csv_file(self, return_list):
        data_list = []
        for result in return_list:
            result = np.array(result).flatten()
            data_list.append(result)

        df = None
        if os.path.exists(self.report_list_path):
            df = pd.read_csv(self.report_list_path, index_col=0)

        df_company_report = pd.DataFrame(data_list)
        df_company_report.dropna(axis=0, inplace=True)
        if df_company_report.shape[0] == 0:
            return

        df_company_report = self._parsing_df_string(df_company_report)
        df = pd.concat([df, df_company_report])
        df.drop_duplicates(["report_id"], inplace=True)
        df.to_csv(self.report_list_path)


    async def async_get_report_list(self, asyncio_util, url, headers, data, doc_code, symbol):
        company_report_list = []
        res = await asyncio_util.async_post_requests(url, asyncio_util.client, headers=headers, data=data)
        bs_obj = bs(res.decode("utf-8"), 'lxml')
        count_bs_obj = bs_obj.select_one("div.page_list>p.page_info")

        if count_bs_obj is None:
            company_report_list = [{
                "disclosure_company" : None,
                "report_link" : None,
                "report_name" : None,
                "issue_company" : None,
                "issue_date" : None,
                "document_type" : None,
                "report_id" : None,
                "symbol" : None,
            }]
            return company_report_list

        text = str.strip(count_bs_obj.text)
        regex = re.compile(r"\[(\d+)/(\d+)\]")
        find_text = regex.search(text)
        for_loop_count = int(find_text.group(2))
        info_list = self._parsing_search_table(bs_obj, doc_code, symbol)
        company_report_list = company_report_list + info_list

        for i in range(2, for_loop_count + 1):
            data["currentPage"] = str(i)
            res = await asyncio_util.async_post_requests(url, asyncio_util.client, headers=headers, data=data)
            bs_obj = bs(res.decode("utf-8"), 'lxml')
            info_list = self._parsing_search_table(bs_obj, doc_code, symbol)
            company_report_list = company_report_list + info_list

        return company_report_list