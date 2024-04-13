import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    start_urls = [
        'https://quotes.toscrape.com/page/1/',
        'https://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        self.log(f'Crawled: {response.url}')
