import scrapy
import os

class IITSpider(scrapy.Spider):
    name = 'iit_spider'
    allowed_domains = ['www.iit.edu']
    start_urls = ['https://www.iit.edu/']
    max_pages = 100  # Max pages to crawl
    pages_crawled = 0
    max_depth = 3  # Max depth to crawl
    output_dir = 'output'  # Define output directory as a class attribute

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={'depth': 0})

    def parse(self, response):
        if self.pages_crawled >= self.max_pages or response.meta.get('depth', 0) > self.max_depth:
            return

        # Save the page
        self.saveFile(response)
        self.pages_crawled += 1
        
        print(f'Parsing page: {response.url}')
        #print(f'Current depth: {response.meta.get("depth", 0)}')
        #print(f'Number of pages crawled: {self.pages_crawled}')
        
        # Follow links to next pages
        for href in response.css('a::attr(href)').getall():
            if href.startswith('http://') or href.startswith('https://'):
                if self.pages_crawled < self.max_pages:
                    yield response.follow(href, self.parse, meta={'depth': response.meta.get('depth', 0) + 1})

    def saveFile(self, response):
        # Ensure the output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Clean and create the filename
        page = response.url.split("/")[-1] or "index"
        filename = f"{page}.html"
        file_path = os.path.join(self.output_dir, filename)
        
        # Write the response to a file
        with open(file_path, 'wb') as file:
            file.write(response.body)
        #print(f'File saved: {filename}')
