import scrapy
 
class MinimalSpider(scrapy.Spider):
    """A menor Scrapy-Aranha do mundo!"""
    name = 'minimal'
    start_urls = [
        'http://www.google.com',
        'http://www.yahoo.com',
    ]
 
    def parse(self, response):
        self.log('ACESSANDO URL: %s' % response.url)