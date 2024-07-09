
from scrapy.crawler import CrawlerProcess
from twisted.internet.defer import Deferred

from node_runner.exceptions import DuplicateError
from node_runner.executions import Execution, Executions


class Executor:

    def __init__(self, process: CrawlerProcess, executions: Executions):
        self.process = process
        self.executions = executions

    def schedule(self, id: str, spider: str, args: dict) -> Deferred:
        for execution in self.executions:
            if execution.id == id:
                raise DuplicateError

        execution = Execution.create(id, self.process.create_crawler(spider))
        self.executions.append(execution)

        def done(_):
            execution.finish()
        
        d = self.process.crawl(execution.crawler, **args)
        d.addBoth(done)

        return d

    def stop(self, id: str) -> bool:
        for execution in self.executions.active():
            if execution.id == id:
                execution.stop()
                return True
        return False
