import scrapy
import json
from problemscraper.items import QuoteObject
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# This spider also handles sites that display data through JS, unlike the previous JS spider however, this one can't
# circumvent having to open up a browser instance to first access the data. Same idea as quotespider essentially, just
# now uses Selenium to open up a browser instance first and then do the same data collection as in the quotespider.
class JavascriptQuoteSpider(scrapy.Spider):
    name = "quotesJSSpider"
    start_urls = ["https://quotes.toscrape.com/js/"]
    start_urls = ["https://quotes.toscrape.com/js"]
    
    def parse(self, response):
        # Not necessarily needed anymore in latest Selenium release but runs much faster
        driver_path = "C:\\Users\\izara\\Desktop\\Projects\\scrape\\chromedriver.exe"
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"


        service = Service(executable_path=driver_path)
        option = webdriver.ChromeOptions()
        option.binary_location = brave_path

        # Makes it so browser isn't visible when running 
        option.add_argument("--headless")

        # Create new browser isntance
        browser = webdriver.Chrome(service=service, options=option)

        browser.get("https://quotes.toscrape.com/js/")

        # Create a new QuoteObject to hold the quote data from the site
        quote = QuoteObject()
        for page_quote in response.css("div.quote"):
            quote['text'] = page_quote.css('span.text::text').get()
            quote['author'] = page_quote.css('small.author::text').get()
            quote['tags'] = page_quote.css('div.tags a.tag::text').getall()
            yield quote

        # Grabs the css containing the text needed to go to the following url
        next_page = response.css("li.next a::attr(href)").extract_first()
        # If the css exists, means there is still more quotes to scrape and keep going until css for next pages can't be found anymore
        if next_page:
            yield response.follow(next_page, callback=self.parse)
       
