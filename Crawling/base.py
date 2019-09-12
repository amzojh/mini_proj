from Util.requestsutil import requestsUtil

class baseCrwaler():
    def __init__(self, logger_class, base_path=None):
        self.webutil = requestsUtil(logger_class)
        self.current_process_url = None
        self.session = None
        if base_path is not None:
            self.base_path = base_path
        else:
            self.base_path = ""
