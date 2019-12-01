# selenium : web application testing framework. Automated testing
import os

from selenium import webdriver # https://github.com/rangyu/TIL/blob/master/python/파이썬-Selenium으로-웹-크롤링하기.md
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from utils import randmized_sleep

class Browser :

    def __init__(self, has_screen = False) : # 전혀 모르겠다.
        dir_path = os.path.dirname(os.path.realpath(__file__)) # __file__ means this file's 
        print("dir_path : " + dir_path)
        service_args = ["--ignore-ssl-errors=true"]
        chrome_options = Options()

        if has_screen is not False :
            print("has_screen : %s" % has_screen)
            chrome_options.add_argument("--headless") # chrome 창을 띄우지 않는 옵션
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(
            executable_path="%s/chromedriver" % dir_path,
            service_args=service_args,
            chrome_options=chrome_options
        )
        self.driver.implicitly_wait(5) # 암시적으로 최대 5초간 대기

    def get(self, url) :
        self.driver.get(url) # url에 접속

    # ??
    def find_one(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver

        if waittime:
            WebDriverWait(obj, waittime).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )

        try:
            return obj.find_element(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None


    # ??
    def find(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver

        try:
            if waittime:
                WebDriverWait(obj, waittime).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
                )
        except TimeoutException:
            return None

        try:
            return obj.find_elements(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None

    def implicitly_wait(self, time) :
        self.driver.implicitly_wait(time)

    # ??
    def scroll_down(self, wait=0.3):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        randmized_sleep(wait)

    def scroll_up(self, offset=-1, wait=2):
        if offset == -1:
            self.driver.execute_script("window.scrollTo(0, 0)")
        else:
            self.driver.execute_script("window.scrollBy(0, -%s)" % offset)
        randmized_sleep(wait)

    @property
    def current_url(self):
        return self.driver.current_url