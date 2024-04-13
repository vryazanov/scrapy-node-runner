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

    def parse(self, response):
        self.log(f'Crawled: {response.url}', level=logging.INFO)

        extractor = scrapy.linkextractors.LinkExtractor()
        for link in extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse)
