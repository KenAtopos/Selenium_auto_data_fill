from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSd-ydbu2hJ3P2f6xLr-2w_Ts1OxbvLIj2lWAjjujCavYrsJMg/viewform?usp=sf_link"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Accept-Language": "en,zh;q=0.9"
}

response = requests.get(url="https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.52894438696289%2C%22east%22%3A-122.33771361303711%2C%22south%22%3A37.618545856678814%2C%22north%22%3A37.931705428257544%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D",
                        headers=headers
                        )

zillow_web = response.text

soup = BeautifulSoup(zillow_web, "html.parser")
# print(soup.prettify())

rent_links = []

links = soup.select(".property-card-data a")
for link in links:
    r_link = link.get("href")
    if "http" not in r_link:
        rent_links.append(f"https://www.zillow.com{r_link}")
    else:
        rent_links.append(r_link)
print(rent_links)

rent_prices = []

prices = soup.select(".hRqIYX span")
for price in prices:
    r_price = price.getText().replace("+ 1 bd", "").replace("/mo", "")
    rent_prices.append(r_price)
print(rent_prices)

rent_address = []

addresses = soup.select("address")
for address in addresses:
    r_address = address.getText().replace("|", ",")
    rent_address.append(r_address)
print(rent_address)

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

chrom_drive_path = "D:\\Software\\Development\\chromedriver.exe"

driver = webdriver.Chrome(service=Service(chrom_drive_path), options=chrome_options)
driver.get(FORM_URL)

for i in range(len(rent_links)):
    time.sleep(2)
    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.send_keys(rent_address[i])
    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.send_keys(rent_prices[i])
    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.send_keys(rent_links[i])
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit.click()
    time.sleep(2)
    re = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    re.click()


