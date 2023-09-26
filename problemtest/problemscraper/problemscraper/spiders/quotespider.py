import scrapy
from problemscraper.items import QuoteObject


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]


    # This will handle basic page pagination where a site's data is split up into multiple different pages via the url
    def parse(self, response):

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