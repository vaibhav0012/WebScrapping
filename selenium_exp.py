from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Paths
website = 'https://www.adamchoi.co.uk/overs/detailed'
chromedriver_path = '/home/vaibhav/chromedriver-linux64/chromedriver'
chrome_binary_path = '/home/vaibhav/chrome-linux64/chrome'

# Configure WebDriver
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary_path

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--headless")  # Optional: Run in headless mode
options.add_argument("--remote-debugging-port=9222")

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.set_page_load_timeout(120)
    driver.get(website)

    # Wait for the "All matches" button
    wait = WebDriverWait(driver, 30)
    all_matches_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//label[@analytics-event="All matches"]'))
    )
    all_matches_button.click()
    print("Button clicked successfully!")

    # Wait to observe behavior
    time.sleep(5)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
