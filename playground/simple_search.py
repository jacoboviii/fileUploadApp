from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Pass in web driver path for webdriver
browser = webdriver.Chrome(r"C:\Users\P2814651\Desktop\Apps\fileUploadApp\chromedriver.exe")

# Navigate to test page
browser.get('http://www.seleniumhq.org')

# select element on page
elem = browser.find_element_by_link_text('Download')

# Get attribute
elem.get_attribute('href')

# Click
elem.click()

# Select Another element
elem2 = browser.find_element_by_link_text('Projects')
elem2.click()

# Search something on serch box
searchBar = browser.find_element_by_id('q')
searchBar.send_keys('download')
searchBar.send_keys(Keys.ENTER)
