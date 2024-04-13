import argparse
import typing

from scrapy.commands import ScrapyCommand
from twisted.internet import endpoints, reactor
from twisted.web import resource, server

from node_runner import zk
from node_runner.executor import Executor
from node_runner.resources import Active, Start, Stop


class NodeRunnerCommand(ScrapyCommand):
    default_settings = {
        'LOG_ENABLED': True,
        'LOG_FORMAT': '%(levelname)s: %(message)s',
    }

    def syntax(self) -> str:
        return '[-v]'

    def short_desc(self) -> str:
        return 'Start a scrapy node'

    def add_options(self, parser: argparse.ArgumentParser) -> None:
        super().add_options(parser)
        parser.add_argument('-p', '--port', type=int, default=8000)
        parser.add_argument('--zk-addr', type=str, default='localhost:2181')
        parser.add_argument('--zk-timeout', type=int, default=1)
        parser.add_argument('--zk-path', type=str, default='/node-runner')

    def run(self, args: typing.List[str], opts: argparse.Namespace) -> None:
        executor = Executor(self.crawler_process)

        index = resource.Resource()
        index.putChild(b'start', Start(executor))
        index.putChild(b'stop', Stop(executor))
        index.putChild(b'active', Active(executor))


        endpoint = endpoints.TCP4ServerEndpoint(reactor, opts.port)
        endpoint.listen(server.Site(index))

        with zk.connect(opts.zk_addr, opts.zk_timeout, opts.zk_path):
            self.crawler_process.start(stop_after_crawl=False)
