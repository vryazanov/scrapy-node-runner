import datetime

from scrapy.crawler import Crawler, CrawlerProcess
from twisted.internet.defer import Deferred

from node_runner.exceptions import DuplicateError


class Executor:

    def __init__(self, process: CrawlerProcess):
        self.process = process
        self.active: dict[str, tuple[Crawler, datetime.datetime]] = {}

    def schedule(self, id: str, spider: str) -> Deferred:
        if id in self.active:
            raise DuplicateError

        crawler = self.process.create_crawler(spider)
        self.active[id] = (crawler, datetime.datetime.now(datetime.UTC))

        def done(_):
            self.active.pop(id)
        
        d = self.process.crawl(crawler)
        d.addBoth(done)

        return d

    def stop(self, id: str) -> bool:
        crawler, _ = self.active.get(id, ('', datetime.datetime.now()))

        if crawler:
            crawler.stop()
