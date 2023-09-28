import scrapy
from problemscraper.items import QuoteObject

# This spider handles infinite scrolling pages by utilizing the API endpoint where the data is sent
# instead. Won't work for every site where data is handled differently but works for the example.
class ScrollSpider(scrapy.Spider):
    name = "scroll"
    start_urls = ["https://quotes.toscrape.com/api/quotes?"]

    def parse(self, response):
        # Accept the data in json format
        data = response.json()

        # For every quote found in the quotes variable
        for quote in data["quotes"]:
            # Create an object using the author name and the quote itself
            yield {
                "Author": quote["author"]["name"],
                "Quote": quote["text"]
            }
        # Grab the current page
        current_page = data["page"]
        # If there are more pages left to scrape, then this field will be true.
        if data["has_next"]:
            # So long as that's the case, create the subsequent url holding new data from the default string plus
            # the current page number + 1
            next_url = "https://quotes.toscrape.com/api/quotes?page=" + str(current_page + 1)
            print("Next url is " + next_url)
            yield scrapy.Request(next_url)
        

    

        