import asyncio
import aiohttp
import time

from requests import ConnectTimeout, ReadTimeout

# get, post request를 위한 함수가 정의되어있음.
# logger : logging을 위한, logger property 
# loop : asynchronous event loop를 


class asynciUtil():

    def __init__(self, logger_class, loop=None):
        self.logger_util = logger_class
        self.logger = logger_class.get_logger()
        self.loop = loop
        self.client = None
    
    def make_loop(self):
        if self.loop is not None:
            self.loop.close()
        self.loop = asyncio.get_event_loop()
    
    def make_client(self, headers=None, cookies=None):
        if self.client is not None:
            self.client.close()
        if self.loop is None:
            self.make_loop()
        
        self.client = aiohttp.ClientSession(loop=self.loop, cookies=cookies, headers=headers)

    async def async_get_requests(self, url, headers=None, cookies=None, timeout=None, params=None,session=None, isReturnSession=False, action=None):

        if self.client is None:
            self.make_client(cookies=cookies)
        
        async with self.client.get(url, headers=headers) as response:
            log_str = self.logger_util.set_web_log_string(url, method='GET', headers=headers, action=action)
            self.logger.info(log_str)
            if response.status != 200:
                self.logger.error("- {} \n request url : {} error has occured".format(self.__class__.__name__, url))
            assert response.status == 200
            result = await response.read() 
        return result

    async def async_post_requests(self, url, client, headers=None, cookies=None, timeout=None, data=None,session=None, isReturnSession=False, action=None):
        if self.client is None:
            self.make_client(cookies=cookies)

        async with client.post(url, headers=headers, data=data) as response:
            log_str = self.logger_util.set_web_log_string(url, method='POST', headers=headers, data=data, action=action)
            self.logger.info(log_str)
            if response.status != 200:
                self.logger.error("- {} \n request url : {} error has occured".format(self.__class__.__name__, url))
            assert response.status == 200
            result = await response.read() 
        return result
