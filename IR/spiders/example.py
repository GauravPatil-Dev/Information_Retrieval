import scrapy

class SimpleSpider(scrapy.Spider):
    name = 'simple'
    start_urls = ['https://www.iit.edu/']

    def parse(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        # Just log response, do not parse
