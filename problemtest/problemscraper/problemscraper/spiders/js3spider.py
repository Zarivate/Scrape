import scrapy
from problemscraper.items import QuoteObject
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from problemscraper.settings import DRIVER_PATH, BRAVE_PATH

# This spider also handles sites that display data through JS, unlike the previous JS spider however, this one can't
# circumvent having to open up a browser instance to first access the data. Same idea as quotespider essentially, just
# now uses Selenium to open up a browser instance first and then do the same data collection as in the quotespider.
class JavascriptQuoteSpider(scrapy.Spider):
    name = "JSSpiderQuotes"
    allowed_domains = ["quotes.toscrape.com/js/"]
    start_urls = ["https://quotes.toscrape.com/js/"]

    
    def parse(self, response):
        # Not necessarily needed anymore in latest Selenium release but runs much faster
        driver_path = DRIVER_PATH
        brave_path = BRAVE_PATH

        service = Service(executable_path=driver_path)
        option = webdriver.ChromeOptions()
        option.binary_location = brave_path

        # Makes it so browser isn't visible when running 
        option.add_argument("--headless")

        # Open browser in incognito mode
        option.add_argument("--incognito")

        # Don't close browser until manually closed
        # option.add_experimental_option("detach", True)

        # Create new browser isntance
        browser = webdriver.Chrome(service=service, options=option)
        browser.get("https://quotes.toscrape.com/js/")

        # All the paths for the data needed to fill out the QuoteObject fields
        quote_path = '//div[@class="quote"]'
        quote_text = './/span[@class="text"]'
        quote_author = './/small[@class="author"]'
        quote_tags = './/a[@class="tag"]'

        # If there is a next page, find the href to go to the next page
        while True:
            try:
                # Grab all the quotes on the page
                quotes = browser.find_elements(By.XPATH, quote_path)
            
                # Create a new QuoteObject to hold the quote data from the site
                quote = QuoteObject()

                # Iterate through every quote
                for element in quotes:
            
                    # Grab the corresponding text and author data from their respective xPaths
                    quote["text"] = element.find_element(By.XPATH, quote_text).text
                    quote["author"] = element.find_element(By.XPATH, quote_author).text

                    # Since there can be multiple tags, they are all first grabbed and stored first
                    tags = element.find_elements(By.XPATH, quote_tags)

                    # Then they are iterated through and joined to fill out the "tags" section of the quote object
                    quote["tags"] = ",".join([tag.text for tag in tags])
                    yield quote
                
                # Sees whether a next page exists, if so there is more data to scrape
                next_page = browser.find_element(By.XPATH, "//*[@class='next']//a[@href]")
                # Click the link to the next page
                next_page.click()
            # For this example, the exception would most likely occur when a failed attempt is made to locate the next_page
            # element on the last page, which there is none. 
            except:
                print("No more pages to scrape")
                break    
        browser.quit()
