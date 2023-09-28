import scrapy
from scrapy.spiders import SitemapSpider
from problemscraper.items import siteMapBlogObject

# This also scrapes all the quotes from the site but uses the siteMap to do so
class SitemapscraperSpider(SitemapSpider):
    name = "SitemapScraper"
    sitemap_urls = ['https://www.scraperapi.com/post-sitemap.xml']
    sitemap_rule = [
     ('blog/', 'parse'),
   ]

# The function itself, follows pattern of previous spiders where an object is created to grab and store the retrieved data. Differs in how
# there is no for each loop, instead simply reiterates itself.
    def parse(self, response):
        blogItem = siteMapBlogObject()
        blogItem["url"] = response.url
        blogItem["title"] = response.css("h1 > span::text").get()
        yield blogItem
