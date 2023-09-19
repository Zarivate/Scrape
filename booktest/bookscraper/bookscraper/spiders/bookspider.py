import scrapy
# Import the created BookItem to be used instead of yielding all the data by itself
from bookscraper.items import BookItem 

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

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
            yield response.follow(book_url, callback=self.parse_book_page)  


        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if "catalogue/" in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page
            yield response.follow(next_page_url, callback=self.parse)


        
    def parse_book_page(self, response):
        
        # Get all the info from the table on the book's product page
        table_rows = response.css("table tr")
        # Create a BookItem object to store all the data
        book_item = BookItem()

         
        book_item["url"] = response.url,
        book_item["title"] = response.css(".product_main h1::text").get(),
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

        
        yield BookItem