# 
# import scrapy
# from scrapy.utils.project import get_project_settings
# #from problemscraper.items import laptopItem
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service



#         # Not necessarily needed anymore in latest Selenium release but runs much faster
# driver_path = "C:\\Users\\izara\\Desktop\\Projects\\scrape\\chromedriver.exe"
# brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

# service = Service(executable_path=driver_path)
# option = webdriver.ChromeOptions()
# option.binary_location = brave_path

#         # Open browser in incognito mode
# #option.add_argument("--incognito")
#         # Don't close browser until manually closed
# option.add_experimental_option("detach", True)
#         # Makes it so browser isn't visible when running 
#         #option.add_argument("--headless")

#         # Create new Instance of the browser
# browser = webdriver.Chrome(service=service, options=option)

# browser.get("https://www.lazada.com.ph/shop-laptops/")

# xpath='//*[@data-qa-locator="product-item"]//a[text()]'

# link_elements = browser.find_elements(By.XPATH, xpath)
# for link_el in link_elements:
#     href = link_el.get_attribute("href")
#     print(href)
        
# browser.quit()
