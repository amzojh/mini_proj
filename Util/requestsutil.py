import requests
import time

from requests import ConnectTimeout, ReadTimeout

# get, post request를 위한 함수가 정의되어있음.


class requestsUtil():

    def __init__(self, logger_class):
        self.logger_util = logger_class
        self.logger = logger_class.get_logger()

    def no_exception_get(self, url, headers=None,cookies=None,timeout=None,params=None,session=None,isReturnSession=False, action=None):


        log_str = self.logger_util.set_web_log_string(url, method='GET', headers=headers, action=action)
        
        self.logger.info(log_str)

        err_cnt=0

        while True:

            if session is not None:
                s = session
            else:
                s = requests.session()
            try:
                ##################### session은 cookie를 아래와 같은 방법으로 넣어줘야함
                if cookies is not None:
                    s.cookies.update(cookies)


                response = s.get(url=url,headers=headers,params=params,timeout=timeout)
                break

            except (ConnectTimeout, ConnectionError, ReadTimeout)  as e:
                if err_cnt < 3:

                    self.logger.critical("[!] 연결오류(GET)")
                    self.logger.critical(type(e))
                    self.logger.critical(e)
                    time.sleep(err_cnt * 5)

                    err_cnt = err_cnt + 1
                    continue

                else:
                    raise e
            
            # connection reset error 발생시 세션을 죽이고 로그인을 재시도
                

            finally:
                if isReturnSession==False:
                    s.close()

        if isReturnSession==False:
            return response
        else:
            return s,response

    def no_exception_post(self, url, headers=None,cookies=None,timeout=None,data=None,session=None,isReturnSession=False, action=None):

        log_str = self.logger_util.set_web_log_string(url, method='POST', headers=headers, data=data, action=action)
        self.logger.info(log_str)
        err_cnt = 0

        while(True):
            if session is not None:
                s = session

            else:
                s = requests.session()
            try:
                ##################### session은 cookie를 아래와 같은 방법으로 넣어줘야함
                if cookies is not None:
                    s.cookies.update(cookies)
                response=s.post(url=url,headers=headers,data=data,timeout=timeout)
                break
            except (ConnectTimeout, ConnectionError, ReadTimeout) as e:
                if err_cnt < 3:

                    self.logger.critical("[!] 연결오류(POST)")
                    self.logger.critical(type(e))
                    self.logger.critical(e)
                    time.sleep(err_cnt * 5)

                    err_cnt = err_cnt + 1
                    continue

                else:
                    raise e
            
            finally:
                if isReturnSession == False:
                    s.close()

        if isReturnSession == False:
            return response
        else:
            return s, response