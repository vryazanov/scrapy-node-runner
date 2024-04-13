from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from twisted.internet.defer import Deferred, DeferredList


class Executor:

    def __init__(self):
        self.runners: dict[str, CrawlerRunner] = {}

    def start(self, id: str, project: str, spider: str, spider_args: dict) -> Deferred:
        settings = Settings()
        settings.setmodule(f'{project}.settings', priority='project')

        runner = CrawlerRunner(settings)

        def done(_):
            self.runners.pop(id)

        self.runners[id] = runner

        d = runner.crawl(spider, *spider_args)
        d.addBoth(done)

        return d

    def stop(self) -> Deferred:
        crawlers: list[Deferred] = []

        for _, runner in self.runners.items():
            for crawler in runner.crawlers:
                crawlers.append(crawler.stop())
        
        return DeferredList(crawlers)

