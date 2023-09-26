# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

# Serializers are used to edit the format of values retrieved from the scraping, this one simply deletes any leading
# values and replaces them with a $. This is normally done in pipelines however but serializers can be good when not
# scraping large data and have little to no need for any pipelines.  
def serialize_price(value):
    return f'$ {str(value)}'

# All the data will now be stored within a BookItem instead of being yielded within the bookspider itself
class BookItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()