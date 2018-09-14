import os
import time
import click
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@click.command()
@click.option('--username', prompt=True,
              default=lambda: os.environ.get('username', ''))
@click.password_option()
def bulk_upload(username, password):
    """Program that automates the bulk upload process."""
    # Contruct path to driver and excel data folder
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filesPath = os.path.join(dirPath, 'PRISM DATA')
    driverPath = os.path.join(dirPath, 'chromedriver')

    driver = webdriver.Chrome(driverPath)
    driver.get('http://charter.osp-cloud.com/ATOM/Dashboard/DashboardHome')

    # Fill in Login Form
    usernameElem = driver.find_element_by_id('username')
    usernameElem.send_keys(username)

    passwordElem = driver.find_element_by_id('password')
    passwordElem.send_keys(password)

    submitBtn = driver.find_element_by_id('submit')
    submitBtn.click()

    # Navigate to Upload form
    bulkAploadLink = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.list-unstyled.menu-item.SidebarMenuUl > li > a#BulkUploadProjects'))
        )
    driver.execute_script("arguments[0].click();", bulkAploadLink)

    # Select all available options from dropdown
    checkBoxOptions = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'form ul > li input[type="radio"]'))
        )
    # Slice first element from list
    checkBoxOptions = checkBoxOptions[1:]
    checkBoxOptionsLen = len(checkBoxOptions)

    # Loop through list of options and upload each file individually
    for i, option in enumerate(checkBoxOptions):
        # Build path to local excel file by grabing parent element text of the option element
        label = driver.execute_script('return arguments[0].parentNode;', option)
        labelText = driver.execute_script('return arguments[0].textContent;', label).strip()
        fileName = labelText + '.xlsx'
        sheetPath = os.path.join(filesPath, fileName)
        # If local excel file exists then begin the upload process
        if os.path.isfile(sheetPath):
            # Select option from dropdown menu
            driver.execute_script("arguments[0].click();", option)
            print('=============================================================================')
            print(f'Selecting Region Market {labelText} - Region {i + 1} of {checkBoxOptionsLen}.')
            # Locate upload file input in form
            fileUpload = driver.find_element_by_css_selector('input[type="file"]')
            # Send file to file upload field
            fileUpload.send_keys(sheetPath)
            print(f'Uploading spreadsheet {fileName}.')
            print('Waiting for sheet validation to be completed...')
            # Click validate button
            validateUploadBtn = driver.find_element_by_id('bulkSaveid')
            driver.execute_script("arguments[0].click();", validateUploadBtn)
            # Wait for loading screen to disappear (modal div with id #loader-wrapper) before moving on the next file
            WebDriverWait(driver, 600).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='loader-wrapper'][contains(@style, 'display: none')]"))
            )
            # Pause script for 20 seconds and display countdown
            # Do not show countdown for the last option
            for j in range(20, 0, -1):
                if checkBoxOptionsLen == (i + 1):
                    break
                print(f' Uploading next sheet in {j} second(s).', end = '\r')
                time.sleep(1)
        else:
            print('=============================================================================')
            print(f'{fileName} was not found in your directory.')

    print('=============================================================================')
    print('Script completed succesfully!')
    input("Press enter to exit ;)")

if __name__ == '__main__':
    print('> Please Enter your ATOM credentials.')
    bulk_upload()