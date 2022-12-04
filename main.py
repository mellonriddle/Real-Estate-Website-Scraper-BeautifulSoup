from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import random

REAL_ESTATE_URL = "https://www.sahibinden.com/kiralik/ankara-cankaya-balgat"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc--HnGDijyivDLumqF3lYC_nYQEFFuPz3IB6LLpTMacAgGKA/viewform"

# Setting up our webdriver
chrome_driver_path = r"C:\Development\chromedriver.exe"
my_service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=my_service)
driver.maximize_window()


# We need to sleep random times occasionally, because we don't want to be blocked on websites
driver.get(REAL_ESTATE_URL)
time.sleep(random.uniform(3, 4))

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Scraping the real estate website for relevant info
titles_raw = soup.find_all(class_="classifiedTitle")
specs_raw = soup.find_all(class_="searchResultsAttributeValue")
price_raw = soup.find_all(class_="classified-price-container")
dates_raw = soup.find_all(class_="searchResultsDateValue")
districts_raw = soup.find_all(class_="searchResultsLocationValue")

# Transforming the data for Google Sheets
titles = []
h_refs = []

for tt in titles_raw:
    titles.append(tt.getText().strip())
    h_refs.append("https://www.sahibinden.com" + tt.get("href"))

specs = [sp.getText().strip() for sp in specs_raw]
rooms = specs[1::2]
square_meters = specs[0::2]

prices = [pr.getText().strip() for pr in price_raw]
dates = [dt.getText().strip().replace("\n\n", " ") for dt in dates_raw]
districts = [ds.getText().strip() for ds in districts_raw]

time.sleep(random.uniform(1, 2))

# Using Google Forms for saving the data to Google Sheets
for i in range(len(titles)):
    driver.get(FORM_URL)
    time.sleep(random.uniform(2, 3))
    inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
    inputs[0].send_keys(titles[i])
    inputs[1].send_keys(h_refs[i])
    inputs[2].send_keys(square_meters[i])
    inputs[3].send_keys(rooms[i])
    inputs[4].send_keys(prices[i])
    inputs[5].send_keys(dates[i])
    inputs[6].send_keys(districts[i])
    buttons = driver.find_elements(By.CSS_SELECTOR, "span span")
    buttons[0].click()
    time.sleep(random.uniform(1, 2))
