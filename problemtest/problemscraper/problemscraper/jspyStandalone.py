# This is a standalone Python file that does the same as js2spider just without the need for any spiders 
import scrapy
#from problemscraper.items import laptopItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from problemscraper.settings import DRIVER_PATH, BRAVE_PATH

# Not necessarily needed anymore in latest Selenium release but runs much faster
driver_path = DRIVER_PATH
brave_path = BRAVE_PATH

service = Service(executable_path=driver_path)
option = webdriver.ChromeOptions()
option.binary_location = brave_path

# Open browser in incognito mode
# option.add_argument("--incognito")

# Don't close browser until manually closed or operation finishes
option.add_experimental_option("detach", True)
# Makes it so browser isn't visible when running 
option.add_argument("--headless")

# Create new Instance of the browser
browser = webdriver.Chrome(service=service, options=option)

browser.get("https://www.lazada.com.ph/shop-laptops/")

# Get the xpath of the product
xpath='//*[@data-qa-locator="product-item"]//a[text()]'

# Find the specific product element using the xPath
link_elements = browser.find_elements(By.XPATH, xpath)

# Fpr every specific product basically
for link_el in link_elements:
    # Grab the href and print it out
    href = link_el.get_attribute("href")
    print(href)
        
browser.quit()
