import scrapy

class ProblemscraperItem(scrapy.Item):
    name = scrapy.Field()
    pass


class QuoteObject(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class siteMapBlogObject(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()