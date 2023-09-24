import scrapy
# Import the created BookItem to be used instead of yielding all the data by itself
from bookscraper.items import BookItem 
import random
from urllib.parse import urlencode

API_KEY = ''
class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com", "proxy.scrapeops.io"]
    start_urls = ["https://books.toscrape.com"]


    # Function that scrapy looks for, used to customize the start urls that will be sent to the proxy provider endpoint
    # def start_request(self):
    #     yield scrapy.Request(url=get_proxy_url(self.start_urls[0]), callback=self.parse)

    # In order to avoid being blocked once too many requests are made, this rotating list of user agents is used
    # user_agent_list = [
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    #     'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    #     'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',    
    # ]

    def parse(self, response):
        # Grab all the books on the current page
        books = response.css("article.product_pod")

        # For every book, grab it's name, price, and url from the corresponding CSS where it's stored  
        for book in books:
            # Grab the relative link for the specific book's product page in the idvidual book's css styling
            relative_url = book.css('h3 a ::attr(href)').get()

            # Due to how some of the site's pages don't always have the same path, check to see what is included
            # in the next_page path before creating the full url
            if "catalogue/" in relative_url:
                # Create the full page's url
                book_url = "https://books.toscrape.com/" + relative_url
            else:
                book_url = "https://books.toscrape.com/catalogue/" + relative_url
            # Go to the following page and call the book_parse function on that response
            # Upon every request, one of the user agents will be chosen among the lists when the call is made. This has to be applied to every response.follow
            # yield response.follow(book_url, callback=self.parse_book_page, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})  
            yield response.follow(book_url, callback=self.parse_book_page)  


        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if "catalogue/" in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page
            # yield response.follow(next_page_url, callback=self.parse, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})
            yield response.follow(next_page_url, callback=self.parse)


        
    def parse_book_page(self, response):
        
        # Get all the info from the table on the book's product page
        table_rows = response.css("table tr")
        # Create a BookItem object to store all the data
        book_item = BookItem()

         
        book_item["url"] = response.url,
        book_item["title"] = response.css(".product_main h1::text").get(),
        book_item["upc"] = table_rows[0].css("td ::text").get(),
        book_item["product_type"] = table_rows[1].css("td ::text").get(),
        book_item["price_excl_tax"] = table_rows[2].css("td ::text").get(),
        book_item["price_incl_tax"] = table_rows[3].css("td ::text").get(),
        book_item["tax"] = table_rows[4].css("td ::text").get(),
        book_item["availability"] = table_rows[5].css("td ::text").get(),
        book_item["num_reviews"] = table_rows[6].css("td ::text").get(),
        book_item["stars"] = response.css("p.star-rating").attrib['class'],
        book_item["category"] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        book_item["description"] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_item["price"] = response.css('p.price_color ::text').get(),

        
        yield book_item


# Function to create a procy url using a third party site and it's credentials
def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url