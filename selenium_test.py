from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

website = 'https://www.adamchoi.co.uk/overs/detailed'
chromedriver_path = '/home/vaibhav/chromedriver-linux64/chromedriver'
chrome_binary_path = '/home/vaibhav/chrome-linux64/chrome'

options = Options()
options.binary_location = chrome_binary_path

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get(website)
driver.quit()