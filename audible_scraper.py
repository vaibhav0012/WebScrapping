import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

website = "https://www.audible.com/search"
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
    driver.maximize_window()
    container = driver.find_element(By.CLASS_NAME,'adbl-impression-container ')
    print('conatiner_fetched')
    # products = container.find_elements(By.XPATH,'./div//span//ul//li[@class="productListItem"]')
    products = container.find_elements(By.XPATH,'.//li[contains(@class, "productListItem")]')
    print('prodicts_fetched')
    # print('products', products)
    headings = []
    subtitles = []
    authors = []
    timeframe = []
    languages = []
    ratings = []
    ratings_count = []
    for product in products:
        # raw_html = product.get_attribute('outerHTML')
        # Remove excess whitespaces, newlines, and tabs
        # cleaned_html = re.sub(r'\s+', ' ', raw_html.strip())
        # print(cleaned_html)
        # print("=" * 80)  # Separator for readability
        # break
        # print(product)
        # //*[@id="center-3"]/div/div/div/span[2]/ul/li[1]/div/div[1]/div/div[2]/div/div/span/ul/li[1]/h3/a
        def get_text(xpath):
            try:
                return product.find_element(By.XPATH, xpath).text
            except:
                return ""
        heading = get_text('.//h3[contains(@class, "bc-heading")]')
        subtitle = get_text('.//li[contains(@class, "subtitle")]')
        author = get_text('.//li[contains(@class, "authorLabel")]')
        length = get_text('.//li[contains(@class, "runtimeLabel")]')
        language = get_text('.//li[contains(@class, "languageLabel")]')
        rating = get_text('.//li[contains(@class, "ratingsLabel")]//span[contains(@class, "bc-pub-offscreen")]')
        rating_count = get_text('.//li[contains(@class, "ratingsLabel")]//span[contains(@class, "bc-color-secondary")]')

        # rating = get_text('.//li[contains(@class, "ratingsLabel")]')

        headings.append(heading)
        # print(td_elements[0].text)
        subtitles.append(subtitle)
        authors.append(author)
        timeframe.append(length)
        languages.append(language)
        ratings.append(rating)
        ratings_count.append(rating_count)
    # Wait for the "All matches" button
    wait = WebDriverWait(driver, 30)

    df = pd.DataFrame({'heading':headings,'authors':authors,'subtitles':subtitles,
                       'timeframe':timeframe,'languages':languages,'ratings':ratings,
                       'ratings_count':ratings_count})
    df.to_csv('books.csv', index = False)
    print(df.head(20))
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()

