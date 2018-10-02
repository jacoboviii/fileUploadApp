import time, os, threading
from pprint import pprint
from printAnimate import loading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

dir_path = os.path.dirname(os.path.realpath(__file__))
driver_path = os.path.join(dir_path, '..', 'chromedriver.exe')
driver = webdriver.Chrome(driver_path)
driver.get('file:///C:/Users/P2814651/Desktop/Apps/fileUploadApp/playground/html_code_02.html')


element = WebDriverWait(driver, 600).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm'][contains(@style, 'display: none')]"))
    )



print('found!')