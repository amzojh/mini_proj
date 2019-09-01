import logging
import os
import datetime


class defaultLogger():
    def __init__(self, name="crawler", file_path=None):
        self.logger = logging.getLogger(name)
        self._set_default_log_conf(file_path)

    def get_logger(self):
        return self.logger

    def set_web_log_string(self, url, method='GET', headers=None, data=None, action=None):
        log_str = f"\nURL : {url}\nMethod : {method}\n"
        
        if headers is not None:
            log_str += f'headers : {headers}\n'
        
        if data is not None:
            log_str += f'Data : {data}\n'

        if action is not None:
            log_str = f'\naction :{action}' + log_str

        return log_str

    def _set_default_log_conf(self, filepath=None):
        
        file_path = os.getcwd() + '/log'
        print(file_path)

        if filepath is not None:
            file_path = filepath

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_formatter = logging.Formatter(fmt='{asctime} - [{levelname}] {message}', style='{')
        stream_formatter = logging.Formatter(fmt='{message}', style='{')

        filename = os.path.join(os.path.dirname(file_path) + '/log', datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S.log'))
        file_handler = logging.FileHandler(filename, 'w')
        stream_handler = logging.StreamHandler()

        file_handler.setFormatter(file_formatter)
        stream_handler.setFormatter(stream_formatter)

        self.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        stream_handler.setLevel(logging.INFO)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
