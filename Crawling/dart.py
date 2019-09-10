from Crawling.base import baseCrwaler
from bs4 import BeautifulSoup as bs
import pandas as pd

class dartCrawler(baseCrwaler):
    def __init__(self, logger_class):
        super().__init__(logger_class)


    def get_report_type(self):
        url = "http://dart.fss.or.kr/"
        res = self.webutil.no_exception_get(url)
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
        df.to_csv("/dart/reportType.csv")

        return df

    def get_all_report_list(self, company_df, start_date="19990101", end_date="20190910"):
        
        symbol_list = company_df["Symbol"].tolist()
        report_type_df = pd.read_csv("/dart/reportType.csv")
        for symbol in symbol_list:
            base_url = f"""
                http://dart.fss.or.kr/dsab001/main.do?autoSearch=true&
                maxResults=100&
                maxLinks=10&
                sort=date&
                series=desc&
                textCrpNm={str(symbol)}&
                finalReport=recent&
                startDate={start_date}&
                endDate={end_date}&
                publicType={}
                """.replace("\n", "")
            res = self.webutil.no_exception_get(base_url ,isReturnSession=True)
            bs_obj = bs(res.text, 'lxml')
            
        # company_df["Symbol"].apply(lambda x: )
