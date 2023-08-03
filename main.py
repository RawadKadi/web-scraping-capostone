from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import lxml

CHROME_PATH="C:\development\chromedriver_win32\chromedriver.exe"
GOOGLE_FORM_PATH="https://docs.google.com/forms/d/e/1FAIpQLScTiHEI2qHp0rE-8QbvVaY8k6jY6IuUichH-BQXSDHNkKZnZg/viewform?usp=sf_link"
RENTAL_LISTING_PATH="https://www.zillow.com/homes/San-Francisco,-CA_rb/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.55177535009766%2C%22east%22%3A-122.31488264990234%2C%22south%22%3A37.69926912019228%2C%22north%22%3A37.851235694487485%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

headers={
    "Accept-Language":"en-US,en;q=0.9",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

response=requests.get(RENTAL_LISTING_PATH,headers=headers)
web_page=response.text
soup=BeautifulSoup(web_page,"lxml")
all_listings=soup.select(".list-card-top a")
listings_in_list=[list.getText() for list in all_listings]


all_links = []
for link in all_listings:
    href = link["href"]
    print(href)
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

all_address=soup.select("list-card-info address")
address_list=[adr_list.getText().split(" | ")[-1] for adr_list in all_address]

all_prices=soup.select("list-card-price")
prices_list=[prs_list.getText().split("+")[0] for prs_list in all_prices]

driver=webdriver.Chrome(executable_path=CHROME_PATH)
for n in range(len(all_links)):

    driver.get(GOOGLE_FORM_PATH)
    time.sleep(2)
    address_answer=driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_answer.send_keys(address_list[n])
    prices_answer=driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prices_answer.send_keys(prices_list[n])
    link_answer=driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_answer.send_keys(listings_in_list[n])
    submit_btn=driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_btn.click()





