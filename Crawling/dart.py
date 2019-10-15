import os
import datetime
import re
import asyncio

import numpy as np
from Crawling.base import baseCrwaler
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

# 내 모듈

# from Database.Model.dart import dartReportType, dartReportList

class dartCrawler(baseCrwaler):
    def __init__(self, logger_class, base_path=None):
        super().__init__(logger_class, base_path)
        self.report_type_path = os.path.join(self.base_path, "/dart/reportType.csv")
        self.report_list_path = os.path.join(self.base_path, "/dart/reportList.csv")


    async def _get_dart_company_list(self, url, headers, asyncio_util):
        base_url = "http://dart.fss.or.kr"
        res = await asyncio_util.async_post_requests(url=url, client=asyncio_util.client, headers=headers)
        bs_obj = bs(res.decode("utf-8"), 'lxml')
        a_tag_list = bs_obj.select("a[href^='/dsae001/selectPopup.ax?selectKey=']")
        task_list = []
        for a_tag in a_tag_list:
            href = a_tag.attrs["href"]
            company_url = base_url + href
            task = asyncio.create_task(self._get_detail_company_data(company_url, headers, asyncio_util))
            task_list.append(task)

        company_detail_list = await asyncio.gather(*task_list)


        return company_detail_list


    """
    result 형태

    회사이름	나가세 엔지니어링 서비스 코리아(주)
    영문명	NAGASE ENGINEERING SERVICE KOREA CO.,LTD.
    공시회사명	나가세엔지니어링서비스코리아
    종목코드	
    대표자명	김재구  대표자명 변경이력
    법인구분	기타법인
    법인등록번호	110111-1458325
    사업자등록번호	213-86-32965
    주소	경기도 안양시 동안구 시민대로 161 925 (비산동, 안양무역센터)
    홈페이지	www.nagase-eng.co.kr
    IR홈페이지	
    전화번호	031-389-0881
    팩스번호	031-389-0884
    업종명	반도체 제조용 기계 제조업
    설립일	1997-09-04
    결산월	03월
    """

    async def _get_detail_company_data(self, url, headers, asyncio_util):
        res = await asyncio_util.async_post_requests(url, client = asyncio_util.client, headers=headers)
        company_dict = {}

        company_id_pattern = re.compile(r"selectKey=(\d+)")
        company_id = re.search(company_id_pattern, url).group(1)

        bs_obj = bs(res.decode("utf-8"), 'lxml')
        td_tag_list = bs_obj.select('table>tbody>tr>td')

        company_dict["company_korean_name"] = str.strip(td_tag_list[0].text)
        company_dict["company_english_name"] = str.strip(td_tag_list[1].text)
        company_dict["company_name"] = str.strip(td_tag_list[2].text)
        company_dict["market_ticker"] = str.strip(td_tag_list[3].text)
        company_dict["CEO"] = str.strip(td_tag_list[4].text)
        company_dict["company_type"] = str.strip(td_tag_list[5].text)
        company_dict["company_registration_number"] = str.strip(td_tag_list[6].text)
        company_dict["business_registration_number"] = str.strip(td_tag_list[7].text)
        company_dict["address"] = str.strip(td_tag_list[8].text)
        company_dict["homepage"] = str.strip(td_tag_list[9].text)
        company_dict["ir_url"] = str.strip(td_tag_list[10].text)
        company_dict["phone_number"] = str.strip(td_tag_list[11].text)
        company_dict["fax"] = str.strip(td_tag_list[12].text)
        company_dict["business_type"] = str.strip(td_tag_list[13].text)
        company_dict["foundation_date"] = str.strip(td_tag_list[14].text)
        company_dict["settlement_month"] = str.strip(td_tag_list[15].text)
        company_dict["company_id"] = str.strip(company_id)

        return company_dict
        
    async def get_all_dart_company_list(self, asyncio_util):

        # 기본 url은 http://dart.fss.or.kr/dsae001/search.ax
        # index는 16개로 이루어짐, 0 - ㄱ , 1 - ㄴ , 2 - ㄷ 등. 한번에 크롤링할 경우 response가 너무 느림.
        index_start_num = 0
        index_num = 0
        base_url = "http://dart.fss.or.kr/dsae001/search.ax"
        task_list = []
        for i in range(index_start_num, index_num):
            search_index = 0
            if i >= 14:
                search_index = i + 1
            else:
                search_index = i
            
            session, res = self.webutil.no_exception_post("http://dart.fss.or.kr/dsae001/main.do", isReturnSession=True)
            cookies = session.cookies
            asyncio_util.make_client(cookies=cookies)
            headers = self._setting_header()
            query_params = {
                "typesOfBusiness" : "all",
                "corporationType" : "all",
                "searchIndex" : str(search_index)
            }

            session, res = self.webutil.no_exception_post(base_url, isReturnSession=True, headers=headers, cookies=cookies, data=query_params)
            bs_obj = bs(res.text, 'lxml')
            count_text = bs_obj.select_one("div.page_list>p.page_info").text
            count_pattern = re.compile(r"\[(\d+)/(\d+)\]")
            count = re.search(count_pattern, count_text).group(2)
            
            for j in range(int(count)):
                query_params["currentPage"] = str(j + 1)
                query_url = base_url + f"?typesOfBusiness=all&corporationType=all&searchIndex={str(search_index)}&currentPage={str(j+1)}"
                task = asyncio.create_task(self._get_dart_company_list(query_url, headers, asyncio_util))
                task_list.append(task)

            result_list = await asyncio.gather(*task_list)
            data_list = []
            for result in result_list:
                result = list(np.array(result).flatten())
                data_list = data_list + result

            df = pd.DataFrame(data_list)
            df.to_excel(f"company_info_{search_index}.xlsx")

        await asyncio_util.client.close()

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
            report_dict["report_link"] = f"{href}"
            report_dict["report_name"] = str.strip(report_info_tag.text)

            report_dict["issue_company"] = str.strip(issue_company_info_tag.text)
            report_dict["issue_date"] = str(date_info_tag.text)
            report_dict["document_type"] = doc_type
            report_dict["report_id"] = rcp_id
            report_dict["symbol"] = symbol
            report_list.append(report_dict)

        return report_list

    def _get_no_duplicated_symbol_list(self, company_df):
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

        symbol_list = self._get_no_duplicated_symbol_list(company_df)

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
        symbol_list = self._get_no_duplicated_symbol_list(company_df)
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
            await self.async_update_at_database(return_list)
            await asyncio_util.client.close()

    async def async_update_at_database(self, return_list):
        data_list = []
        for result in return_list:
            result = np.array(result).flatten()
            data_list = data_list + result

        df_company_report = pd.DataFrame(data_list)
        df_company_report.dropna(axis=0, inplace=True)

        if df_company_report.shape[0] == 0:
            return

        df_company_report = self._parsing_df_string(df_company_report)
        df_company_report.drop_duplicates(["report_id"], inplace=True)
        df_company_report.to_csv(self.report_list_path)


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