from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Not necessarily needed anymore in latest Selenium release but runs much faster
driver_path = ""
brave_path = ""

service = Service(executable_path=driver_path)
option = webdriver.ChromeOptions()
option.binary_location = brave_path

# Open browser in incognito mode
option.add_argument("--incognito")
# Don't close browser until manually closed
option.add_experimental_option("detach", True)
# option.add_argument("--headless") OPTIONAL

# Create new Instance of the browser
browser = webdriver.Chrome(service=service, options=option)

browser.get("https://www.google.com")