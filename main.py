from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pprint import pprint
import requests
from bs4 import BeautifulSoup
global webdriver


zillow_website = "https://www.zillow.com"
zillow_endpoint = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.69219435644531%2C%22east%22%3A-122.17446364355469%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D'
google_forms_endpoint = "https://forms.gle/9KEFqdSfGTJiizao9"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.88 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}

response = requests.get(url=zillow_endpoint, headers=headers)
response.raise_for_status()
zillow_webpage = response.text
soup = BeautifulSoup(zillow_webpage, "html.parser")
property_links = [link.attrs.get("href") for link in soup.select(selector=".list-card-info > .list-card-link[href]")]
property_prices = [price.text.replace(",", "").split(" ")[0].strip("$/mo,bds+") for price in
                   soup.select(selector=".list-card-price")]
property_addresses = [address.text.split(" | ")[-1] for address in soup.select(selector="address, .list-card-addr")]

for link in property_links:
    if "zillow" in link:
        pass
    else:
        link_index = property_links.index(link)
        property_links[link_index] = f"{zillow_website}{link}"

print("selenium time")

chrome_driver_path = "C:\Development\chromedriver.exe"
s = Service(chrome_driver_path)
driver = webdriver.Chrome(service=s)


for i in range(len(property_prices)):
    driver.get(google_forms_endpoint)

    address_input = driver.find_elements(by=By.CSS_SELECTOR, value=".whsOnd, .zHQkBf")[0]
    price_input = driver.find_elements(by=By.CSS_SELECTOR, value=".whsOnd, .zHQkBf")[1]
    link_input = driver.find_elements(by=By.CSS_SELECTOR, value=".whsOnd, .zHQkBf")[2]
    submit_button = driver.find_element(by=By.XPATH,
                                        value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    print(address_input)
    address_input.send_keys(property_addresses[i])
    price_input.send_keys(property_prices[i])
    link_input.send_keys(property_links[i])
    submit_button.click()
