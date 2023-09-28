import scrapy
from problemscraper.items import QuoteObject

# This spider handles scraping data from pages where data is displayed through Javascript, meaning it's not static.
class JavascriptSpider(scrapy.Spider):
    name = "scroll"
    start_urls = ["https://quotes.toscrape.com/api/quotes?"]

    def parse(self, response):
        data = response.json()

        for quote in data["quotes"]:
            yield {
                "Author": quote["author"]["name"],
                "Quote": quote["text"]
            }
        current_page = data["page"]
        if data["has_next"]:
            next_url = "https://quotes.toscrape.com/api/quotes?page=" + str(current_page + 1)
            print("Next url is " + next_url)
            yield scrapy.Request(next_url)
        

    

        