from selenium import webdriver

from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotSelectableException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

default_trial = 3

class seleniumUtil:
    
    def __init__(self, logger=None, trial=3):
        self.driver = self.selenium_main()
        self.trial = trial
        pass


    def find_element_until_finding_by_element(self, base_element, css, trial=default_trial):
        isSelected = False
        cnt = 0
        while not isSelected:
            try:
                element = base_element.find_element_by_css_selector(css)
                isSelected = True
            except NoSuchElementException:
                if cnt > trial:
                    raise NoSuchElementException("element를 얻어오는데 문제가 생겼습니다.")
                cnt += 1

        return element

    def find_elements_until_finding_by_element(self, base_element, css, trial=default_trial):
        isSelected = False
        cnt = 0
        while not isSelected:
            try:
                element = base_element.find_elements_by_css_selector(css)
                isSelected = True
            except NoSuchElementException:
                if cnt > trial:
                    raise NoSuchElementException("element를 얻어오는데 문제가 생겼습니다.")
                cnt += 1
        
        return element


    def find_element_until_finding(self, css, trial=default_trial):
        isSelected = False
        cnt = 0
        while not isSelected:
            try:
                element = self.driver.find_element_by_css_selector(css)
                isSelected = True
            except NoSuchElementException:
                if cnt > trial:
                    raise NoSuchElementException("element를 얻어오는데 문제가 생겼습니다.")
                cnt += 1

        return element

    def ischecked_web_element(self, css, trial=default_trial):
        isSelected = False
        cnt = 0
        while not isSelected:
            try:
                element = self.driver.find_element_by_css_selector(css)
                isSelected = True
            except NoSuchElementException:
                if cnt > trial:
                    return False
                cnt += 1

        return True


    def find_elements_until_finding(self, css, trial=default_trial):
        isSelected = False
        cnt = 0
        while not isSelected:
            try:
                element = self.driver.find_element_by_css_selector(css)
                isSelected = True
            except NoSuchElementException:
                if cnt > trial:
                    raise NoSuchElementException("element를 얻어오는데 문제가 생겼습니다.")
                cnt += 1
                
        return element


    def find_and_element_until_click(self, css, trial=default_trial):
        isClicked = False
        cnt = 0
        while not isClicked:
            try:
                element = self.find_element_until_finding(css, trial=1)
                self.driver.execute_script('arguments[0].click()', element)
                isClicked = True
            except ElementNotSelectableException:
                if cnt > trial:
                    raise ElementNotSelectableException()
                cnt += 1
            
            except NoSuchElementException:
                raise NoSuchElementException("CSS틀렸다")

    def click_until_seccess(self, element, css, trial=default_trial):
        isClicked = False
        cnt = 0
        while not isClicked:
            try:
                self.driver.execute_script('arguments[0].click()', element)
                isClicked = True
            except Exception:
                if cnt > trial:
                    raise ElementNotSelectableException()
                cnt += 1
   
    
    def selenium_main(self):
        options = webdriver.ChromeOptions()
        options.add_argument("disable-extensions")
        options.add_argument("start-maximized")
        options.add_experimental_option("useAutomationExtension",False)
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-setuid-sandbox")

        #options.add_argument("--headless")
        options.add_argument("--log-level=3")
        options.add_argument("--kiosk-printing")

        options.add_experimental_option('prefs', {
            # "download.default_directory": base_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        driver = webdriver.Chrome("C:/ChromeDriver/chromedriver.exe",chrome_options=options)
        driver.implicitly_wait(3)

        return driver