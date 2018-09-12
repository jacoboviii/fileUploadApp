import os
from glob import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Contruct path to driver and all excel files
dir_path = os.path.dirname(os.path.realpath(__file__))
file_list = glob(os.path.join(dir_path,'*.xlsx'))
driver_path = os.path.join(dir_path, 'chromedriver')

driver = webdriver.Chrome(driver_path)
driver.get('http://localhost:5000/upload')

# Loop through all the files
for file in file_list:
    file_upload = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "file-upload"))
    )

    # Upload file
    file_upload.send_keys(file)

    # Click on process file
    processBtn = driver.find_element_by_css_selector('.button-process.button.is-info')
    processBtn.click()

    # Download file
    downloadBtn = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.button-download.button.is-success'))
    )
    downloadBtn.click()