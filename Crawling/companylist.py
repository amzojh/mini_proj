from Crawling.base import baseCrwaler

class companyListCrwaler(baseCrwaler):
    def __init__(self, logger_class):
        super().__init__(logger_class)

    def process(self):
        page_index = 1

        for page_index in range(1, 25):
            base_url = f"""
                https://dev-kind.krx.co.kr/corpgeneral/corpList.do?method=searchCorpList&pageIndex={str(page_index)}&currentPageSize=100&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=13&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all
                """

            print(base_url)