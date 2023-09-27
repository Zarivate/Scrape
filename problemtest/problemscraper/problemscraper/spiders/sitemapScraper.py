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

    def parse(self, response):
        blogItem = siteMapBlogObject()
        blogItem["url"] = response.url
        blogItem["title"] = response.css("h1 > span::text").get()
        yield blogItem
