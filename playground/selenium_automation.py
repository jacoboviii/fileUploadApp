from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

# Python-Selenium Frame Work
# Contruct path to driver and all excel files

"""
dir_path = os.path.dirname(os.path.realpath(__file__))
driver_path = os.path.join(dir_path, '../', 'chromedriver')

driver = webdriver.Chrome(driver_path)
driver.get('http://www.python.org')

elem = driver.find_element_by_name('q')
elem.clear()
elem.send_keys('pycon')
elem.send_keys(Keys.RETURN)
time.sleep(8)

driver.close()
"""

## Parsin the html DOM Structure

dir_path = os.path.dirname(os.path.realpath(__file__))
driver_path = os.path.join(dir_path, '../', 'chromedriver')
driver = webdriver.Chrome(driver_path)
driver.get('file:///Users/jacoboperez/Desktop/Coding_Bootcamp.nosync/fileUploadApp/playground/html_code_02.html')

# Locate elements by id and name
login_form = driver.find_element_by_id('loginForm')
username = driver.find_element_by_name('username')

# Locate using XML paths: absolute and relative paths
login_form_absolute = driver.find_element_by_xpath('/html/body/form[1]')
login_form_relative = driver.find_element_by_xpath('//form[1]')
login_form_id = driver.find_element_by_xpath('//form[@id="loginForm"]')

# Locate elements by class
content = driver.find_elements_by_class_name('content')

print('login', login_form)
print('username', username)
print('login absolute', login_form_absolute)
print('login relative', login_form_relative)
print('login relative with id', login_form_id)
print('content', content)

driver.close()