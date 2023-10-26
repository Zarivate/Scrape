import scrapy
from problemscraper.items import QuoteObject


# Another spider to handle retreiving the same styled quote content. Only slight difference is that it's in table form now.
# Isn't JS rendered so isn't necessary to use Selenium.
class QuotespiderSpider(scrapy.Spider):
    name = "table"
    allowed_domains = ["https://quotes.toscrape.com/tableful/"]
    start_urls = ["https://quotes.toscrape.com/tableful/"]


    # Main idea for now is, since there can be multiple tags for 1 quote, but only 1 quote for each set of quotes. Grab all the quotes first,
    # once you have that, use the length of them to iterate through until the end of both the quotes and the set of tags. IE:
    # There are 10 quotes on the page so would be of length 10. Grab the first quote and the first set of quotes and apply them to the first quoteObject
    # and so forth. Make sure to splice the quote string though to get the Author by the way.
    def parse(self, response):

        # Create a new QuoteObject to hold the quote data from the site
        quote = QuoteObject()
        
        quotes = response.xpath('//td[contains(@style, "padding-top")]/text()').getall()
        tags = response.xpath('//td[contains(@style, "padding-bottom")]/text()').getall()
        print(len(quotes))
        for quote in quotes:
            
            author = quote.split("Author: ")[1]
            print(author)
            
        
        

        

        
# Table problem 
# XPATH for first quote *//td[contains(@style, "padding-top")]  
# XPath for first set of tags //td[contains(@style, "padding-bottom")][1]