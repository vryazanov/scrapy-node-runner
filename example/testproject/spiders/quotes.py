import logging

import scrapy
import scrapy.linkextractors


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = [
        'quotes.toscrape.com',
    ]
    start_urls = [
        'https://quotes.toscrape.com/'
    ]

    def __init__(self, limit: int = 10):
        self.limit = limit

    def parse(self, response):
        self.log(f'Limit: {self.limit}. Crawled: {response.url}', level=logging.INFO)

        extractor = scrapy.linkextractors.LinkExtractor()
        for idx, link in enumerate(extractor.extract_links(response)):
            if idx < self.limit:
                yield scrapy.Request(link.url, callback=self.parse)
