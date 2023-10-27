import scrapy
from scrapy import Spider
from scrapy.http import FormRequest
from problemscraper.items import QuoteObject


# A program for handling simple logins that accept any input username and password. The trick for this one is making sure to find and send in
# the necessary csrf token along with the form request when logging in. 
class HiddenDataLoginSpider(Spider):
    name = 'loginSimple'

    # Function to start, makes simple request to main url that calls another function that handles the actual logging in
    def start_requests(self):
        login_url = 'http://quotes.toscrape.com/login'
        yield scrapy.Request(login_url, callback=self.login)
    
    # Function that handles logging in, gets the corresponding csrf token from a hidden input field on the main login and
    # sends it in alongside the form request to successfully login.
    def login(self, response):
        token = response.css("form input[name=csrf_token]::attr(value)").extract_first()
        yield FormRequest.from_response(response,
                                         formdata={'csrf_token': token,
                                                   'password': 'anythingworks',
                                                   'username': 'anythingworks'},
                                         callback=self.start_scraping)

    def start_scraping(self, response):
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
            yield response.follow(next_page, callback=self.start_scraping)
