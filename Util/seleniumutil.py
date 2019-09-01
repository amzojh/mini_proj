from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotSelectableException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

default_trial = 10

class seleniumUtil:
    
    def __init__(self, logger=None, trial=10):
        pass

    def find_element_until_finding(self, driver, xpath, trial=default_trial):
        isSelected = False
        cnt = 0
        while not isSelected:
            try:
                element = driver.find_element_by_xpath(xpath)
                isSelected = True
            except NoSuchElementException:
                if cnt > trial:
                    raise NoSuchElementException("element를 얻어오는데 문제가 생겼습니다.")
                cnt += 1

        return element

    def ischecked_web_element(self, driver, xpath, trial=default_trial):
        isSelected = False
        cnt = 0
        while not isSelected:
            try:
                element = driver.find_element_by_xpath(xpath)
                isSelected = True
            except NoSuchElementException:
                if cnt > trial:
                    return False
                cnt += 1

        return True


    def find_elements_until_finding(self, driver, xpath, trial=default_trial):
        isSelected = False
        cnt = 0
        while not isSelected:
            try:
                element = driver.find_elements_by_xpath(xpath)
                isSelected = True
            except NoSuchElementException:
                if cnt > trial:
                    raise NoSuchElementException("element를 얻어오는데 문제가 생겼습니다.")
                cnt += 1
                
        return element


    def find_and_element_until_click(self, driver, xpath, trial=default_trial):
        isClicked = False
        cnt = 0
        while not isClicked:
            try:
                element = self.find_element_until_finding(driver, xpath, 2)
                driver.execute_script('arguments[0].click()', element)
                isClicked = True
            except ElementNotSelectableException:
                if cnt > trial:
                    raise ElementNotSelectableException()
                cnt += 1
            
            except NoSuchElementException:
                raise NoSuchElementException("CSS틀렸다")

    def click_until_seccess(self, driver, element, css, trial=default_trial):
        isClicked = False
        cnt = 0
        while not isClicked:
            try:
                driver.execute_script('arguments[0].click()', element)
                isClicked = True
            except Exception:
                if cnt > trial:
                    raise ElementNotSelectableException()
                cnt += 1
   
   