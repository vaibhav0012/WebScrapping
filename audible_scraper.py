import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

website = "https://www.audible.in/search"
chromedriver_path = '/home/vaibhav/chromedriver-linux64/chromedriver'
chrome_binary_path = '/home/vaibhav/chrome-linux64/chrome'

# Configure WebDriver
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary_path

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
# options.add_argument("--headless")  # Optional: Run in headless mode
options.add_argument("--remote-debugging-port=9222")

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.set_page_load_timeout(120)
    driver.get(website)
    driver.maximize_window()

    # Pagination
    pagination = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, './/ul[contains(@class,"pagingElements")]'))
    )
    pages = pagination.find_elements(By.XPATH, 'li')
    last_page = int(pages[-2].text)

    curr_page = 1
    headings, subtitles, authors, timeframe, languages, ratings, ratings_count = [], [], [], [], [], [], []

    while curr_page <= last_page:
        print(f"Scraping page {curr_page} of {last_page}...")

        # Wait for container
        container = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container'))
        )
        print('Container fetched')

        products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')
        print(f'{len(products)} products fetched')

        for product in products:
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

            headings.append(heading)
            subtitles.append(subtitle)
            authors.append(author)
            timeframe.append(length)
            languages.append(language)
            ratings.append(rating)
            ratings_count.append(rating_count)

        # Go to the next page
        curr_page += 1
        try:
            next_page = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[contains(@class,"nextButton")]'))
            )
            next_page.click()
        except Exception as e:
            print(f"Could not navigate to next page: {e}")
            break

    # Save to CSV
    df = pd.DataFrame({
        'heading': headings,
        'authors': authors,
        'subtitles': subtitles,
        'timeframe': timeframe,
        'languages': languages,
        'ratings': ratings,
        'ratings_count': ratings_count
    })
    df.to_csv('books.csv', index=False)
    print(df.head(20))

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
