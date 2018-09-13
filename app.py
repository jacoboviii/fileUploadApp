import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Contruct path to driver and all excel files
dir_path = os.path.dirname(os.path.realpath(__file__))
files_path = '/Users/jacoboperez/Desktop/Coding_Bootcamp.nosync/fileUploadApp/PRISM DATA/'
driver_path = os.path.join(dir_path, 'chromedriver')

driver = webdriver.Chrome(driver_path)
driver.get('http://charter.osp-cloud.com/ATOM/Dashboard/DashboardHome')

# Login Form
username = 'P2814651'
password = 'Cheguevara!67'

usernameElem = driver.find_element_by_id('username')
usernameElem.send_keys(username)

passwordElem = driver.find_element_by_id('password')
passwordElem.send_keys(password)

submitBtn = driver.find_element_by_id('submit')
submitBtn.click()

# Navigate to Upload form
bulkAploadLink = driver.find_element_by_css_selector('ul.list-unstyled.menu-item.SidebarMenuUl > li > a#BulkUploadProjects')
driver.execute_script("arguments[0].click();", bulkAploadLink)


# Select all available options from dropdown
checkBoxOptions = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'form ul > li input[type="radio"]'))
    )

# Loop through list of options and upload each file individually
for option in checkBoxOptions:
    label = driver.execute_script('return arguments[0].parentNode;', option)
    labelText = driver.execute_script('return arguments[0].textContent;', label).strip()
    fileData = os.path.join(files_path, labelText + '.xlsx')
    print(f'{fileData}')
    if os.path.isfile(fileData):
        # Select option first
        time.sleep(3)
        driver.execute_script("arguments[0].click();", option)
        print(f'{labelText} was selected')
        # Upload file to form
        fileUpload = driver.find_element_by_css_selector('input[type="file"]')
        fileUpload.send_keys(fileData)
    else:
        print('File does not exist')

# validateUploadBtn = driver.find_element_by_id('bulkSaveid')
# driver.execute_script("arguments[0].click();", validateUploadBtn)

# Patrick Folder
# C:\Users\P2141641\Desktop\PRISM DATA\