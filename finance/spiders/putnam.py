import scrapy


class PutnamSpider(scrapy.Spider):
    name = 'putnam'
    allowed_domains = ['www.putnam.com']
    start_urls = ['https://www.putnam.com/literature/pdf/TX001-6a6398e1779dd03e057b2f6f9972ee58.pdf']

    def parse(self, response):
        pass
