from Util.requestsutil import requestsUtil

class baseCrwaler():
    def __init__(self, logger_class):
        self.webutil = requestsUtil(logger_class)
        self.current_process_url = None
        self.session = None