import scrapy
from problemscraper.items import QuoteObject
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# This spider also handles sites that display data through JS, unlike the previous JS spider however, this one can't
# circumvent having to open up a browser instance to first access the data. Same idea as quotespider essentially, just
# now uses Selenium to open up a browser instance first and then do the same data collection as in the quotespider.
class JavascriptQuoteSpider(scrapy.Spider):
    name = "quotesJSSpider"
    
    def start_requests(self):
        # Not necessarily needed anymore in latest Selenium release but runs much faster
        driver_path = "C:\\Users\\izara\\Desktop\\Projects\\scrape\\chromedriver.exe"
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

        service = Service(executable_path=driver_path)
        option = webdriver.ChromeOptions()
        option.binary_location = brave_path

        # Makes it so browser isn't visible when running 
        option.add_argument("--headless")

        # Open browser in incognito mode
        option.add_argument("--incognito")

        # Don't close browser until manually closed
        option.add_experimental_option("detach", True)

        # Create new browser isntance
        browser = webdriver.Chrome(service=service, options=option)
        browser.get("https://quotes.toscrape.com/js/") 

        # All the paths for the data needed to fill out the QuoteObject fields
        quote_path = '//div[@class="quote"]'
        quote_text = './/span[@class="text"]'
        quote_author = './/small[@class="author"]'
        quote_tags = './/a[@class="tag"]'

        # Grab all the quotes on the page
        quotes = browser.find_elements(By.XPATH, quote_path)
        
        # Create a new QuoteObject to hold the quote data from the site
        quote = QuoteObject()

        # Iterate through every quote
        for element in quotes:
            # There can be multiple tags so an array is used to store them all and to append to the "tags" field later
            tag_list = []
            quote["text"] = element.find_element(By.XPATH, quote_text).text
            quote["author"] = element.find_element(By.XPATH, quote_author).text
            # Iterate through every tag
            for tag in element.find_elements(By.XPATH, quote_tags):
                # Add them to the list
                tag_list.append(tag.text)
            # Set the field to be equal to the list
            quote["tags"] = tag_list
            yield quote
        
        # Sees whether a next page exists, if so there is more data to scrape
        next_page = browser.find_element(By.XPATH, "//*[@class='next']//a[@href]")

        # If there is a next page, find the href to go to the next page
        if next_page:
            # This is another way of doing it which is having the browser manually click the link
            # next_link = next_page.find_element(By.XPATH, ".//a[@href]").click()
            href = next_page.get_attribute("href") 
            print(href)
            yield scrapy.Request(href, callback=self.parse)
        browser.quit()
            
# Function that creates a laptopItem using the passed in response
    def parse(self, response):
        quote = QuoteObject()
        laptop["price"] = response.css(".pdp-price_color_orange ::text").get()
        laptop["name"] = response.css("h1 ::text").get()
        yield laptop
