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
    # and so forth. Make sure to splice the quote string though to get the Author by the way. Similar idea for the tags, they're in a separate row
    # and not included in the same table body/section as the quotes.
    def parse(self, response):

        # Create a new QuoteObject to hold the quote data from the site
        quote = QuoteObject()
        
        # Since it's a table, first grab the quotes 
        quotes = response.xpath('//td[contains(@style, "padding-top")]/text()').getall()

        # The tags for the first quote start at the 3rd so set a variable for it
        num = 3

        # Iterate through the quotes
        for single_quote in quotes:
            quote['text'] = single_quote.split(" Author: ")[0].replace('\n', '')
            quote["author"] = single_quote.split("Author: ")[1]
            quote["tags"] = response.xpath(f'//tr[{num}]//td/a/text()').getall()

            # The 2nd following row holds the subsequent quote's tags so increment the row number by 2 to grab the next quote's tags
            num += 2
            yield quote
            