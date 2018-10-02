import os
import glob
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
    # Contruct paths
    dirPath = os.path.dirname(os.path.realpath(__file__))
    filesPath = os.path.join(dirPath, 'PRISM DATA')
    falloutPath = os.path.join(dirPath, 'FALLOUT DATA')
    driverPath = os.path.join(dirPath, 'chromedriver')
    pattern = os.path.join(dirPath, 'FALLOUT DATA/*.xlsx')

    # Move old error reports to archive folder
    print('Archiving reports under ARCHIVE folder...')
    oldReport = glob.glob(pattern)
    for f in oldReport:
        new_file = f.replace('FALLOUT DATA', 'FALLOUT DATA/ARCHIVE')
        os.rename(f, new_file)

    # Chrome Options
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": falloutPath,
        "profile.default_content_setting_values.automatic_downloads": 1,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(executable_path=driverPath, options=options)
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
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'ul.list-unstyled.menu-item.SidebarMenuUl > li > a#BulkUploadProjects'))
    )
    driver.execute_script("arguments[0].click();", bulkAploadLink)

    # Select all available options from dropdown
    checkBoxOptions = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'form ul > li input[type="radio"]'))
    )
    # Drop first element from list
    checkBoxOptions = checkBoxOptions[1:]
    checkBoxOptionsLen = len(checkBoxOptions)

    # Loop through list of options and upload each file individually
    optionsDict = {}
    for i, option in enumerate(checkBoxOptions):
        # Build path to local excel file by grabbing parent element's text of option
        label = driver.execute_script(
            'return arguments[0].parentNode;', option)
        labelText = driver.execute_script(
            'return arguments[0].textContent;', label).strip()
        fileName = labelText + '.xlsx'
        sheetPath = os.path.join(filesPath, fileName)
        # If local excel file exists then begin the upload process
        if os.path.isfile(sheetPath):
            # Select an option from dropdown menu
            driver.execute_script("arguments[0].click();", option)
            print(
                '=============================================================================')
            print(
                f'Selecting Region Market {labelText} - Region {i + 1} of {checkBoxOptionsLen}.')
            # Locate upload file input in form
            fileUpload = driver.find_element_by_css_selector(
                'input[type="file"]')
            # Send file to file upload field
            fileUpload.send_keys(sheetPath)
            print(f'Uploading spreadsheet {fileName}.')
            # Click validate button
            print('Waiting for sheet validation to be completed...')
            validateUploadBtn = driver.find_element_by_id('bulkSaveid')
            driver.execute_script("arguments[0].click();", validateUploadBtn)
            # Wait for loading screen to disappear (modal div with id #loader-wrapper) before moving on the next file
            WebDriverWait(driver, 600).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='loader-wrapper'][contains(@style, 'display: none')]"))
            )
            # Grab error message from label with #ErrorMessage and add new entry to dictionary
            erroMessage = driver.find_element_by_id('ErrorMessage').text
            optionsDict[labelText] = [fileName, erroMessage]

            # Pause script for 5 seconds and display countdown
            # Do not show countdown for the last option
            for j in range(5, 0, -1):
                if checkBoxOptionsLen == (i + 1):
                    print(
                        f' Wainting for last error report to get downloaded: {j} second(s).', end='\r')
                    time.sleep(1)
                print(f' Uploading next sheet in {j} second(s).', end='\r')
                time.sleep(1)
        else:
            print(
                '=============================================================================')
            print(f'{fileName} was not found in the PRISM DATA folder.')

    # Rename newly created reports to market area name
    print('Renaming new reports...')
    newReports = glob.glob(pattern)
    # Sort files by created date
    newReports.sort(key=os.path.getmtime)

    # Loop throung dictionary
    for i, (key, value) in enumerate(optionsDict.items()):
        print(f'{key} corresponds to {value} and {newReports[i]}')
        old_name = newReports[i]
        new_name = old_name.replace('EZTracking_BulkUploadErrorReport', key)
        os.rename(old_name, new_name)

    print('=============================================================================')
    print('Script completed succesfully!')
    input("Press enter to exit ;)")


if __name__ == '__main__':
    print('> Please Enter your ATOM credentials.')
    bulk_upload()
