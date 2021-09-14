from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

ZILLOW_PASSWORD = "23ldsDdDD_98J"
ZWSID = "X1-ZWz16ieo1u24gb_98wrk"


GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSfxYaMvqve0wss0ZP8pkb93SMOpq463pQWQzhN3R1rJe9VWuw/viewform?usp=sf_link"
ZILLOW_LINK = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.61529005957031%2C%22east%22%3A-122.25136794042969%2C%22south%22%3A37.65026580406369%2C%22north%22%3A37.90010602785949%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"

data = {
    "ZWSID": "X1-ZWz16ieo1u24gb_98wrk",
}

zillow_headers = {
    #'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    #'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}
response = requests.get(url=ZILLOW_LINK, params=data, headers=zillow_headers)
soup = BeautifulSoup(response.content, "html.parser")



count = 0
links = []
tags = soup.select('article div a')
for t in tags:
    tag = t.get("href")
    if "https" not in tag:
        links.append(f"https://www.zillow.com{tag}")
    else:
        links.append(tag)

links = list(dict.fromkeys(links))
for link in links:
    count += 1
    print(count)
    print(link)

count = 0
address = []
address_lines = soup.select('.list-card-addr')
for a in address_lines:
    add = a.text
    if " | " in add:
        add = add.split(" | ")[1]
        count += 1
        print(count)
        print(add)
        if add not in address:
            address.append(add)
    if add not in address:
        address.append(add)
address = list(dict.fromkeys(address))
for add in address:
    count += 1
    print(count)
    print(add)

count = 0
prices = []
price_line_codes = soup.select('.list-card-price')
for p in price_line_codes:
    pr = p.text
    if pr is None:
        count += 1
        print(count)
        print("price not found")
    count += 1
    print(count)
    price_individual = pr[:6]
    print(price_individual)
    prices.append(price_individual)

DRIVER_PATH = "C://Development/chromedriver.exe"
driver = webdriver.Chrome(DRIVER_PATH)


for n in range(len(links)):
    time.sleep(2)
    driver.get(GOOGLE_FORM_LINK)


    address_field = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_field.send_keys(address[n])
    price_field = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_field.send_keys(prices[n])
    link_field = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field.send_keys(links[n])

    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    submit_button.click()