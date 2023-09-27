import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from problemscraper.items import QuoteObject

# CrawlSpiders are best used for when needing to retrieve information from pages of a specific type, it's why the Rule and LinkExtractor
# are necessary. 
class QuotesSpider(CrawlSpider):
    name = "testcrawlspider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

# For the rule here, all pages that have 'page/' in their url are scraped but any that also have 'tag/' are excluded. This is to avoid
# scraping the tag pages as well as they include 'page/' in their url. 
    rules = (
        Rule(LinkExtractor(allow = 'page/', deny='tag/'), callback='parse', follow=True),
    )
    
    def parse(self, response):
        # Create a QuoteObject to hold scraped information
        quote_item = QuoteObject()
        # For every quote found, store it's corresponding info within the matching QuoteObject parameter.
        for quote in response.css('div.quote'):
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item