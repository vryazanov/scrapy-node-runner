
import argparse
import signal
import socket

from kazoo.client import KazooClient
from scrapy.utils.log import configure_logging
from twisted.internet import endpoints
from twisted.web import resource, server

from node_runner import zk
from node_runner.executor import Executor
from node_runner.reactor import get_reactor
from node_runner.resources.start import Start

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8000)
    parser.add_argument('--zk-addr', type=str, default='localhost:2181')
    parser.add_argument('--zk-timeout', type=int, default=1)
    parser.add_argument('--zk-path', type=str, default='/node-runner')
    return parser.parse_args()


def init_site(executor: Executor) -> server.Session:
    index = resource.Resource()
    index.putChild(b'start', Start(executor))

    return server.Site(index)

if __name__ == '__main__':
    args = parse_args()

    executor = Executor()
    site = init_site(executor)

    reactor = get_reactor()

    endpoint = endpoints.TCP4ServerEndpoint(reactor, args.port)
    endpoint.listen(site)

    def shutdown(*_):
        d = executor.stop()
        d.addBoth(lambda _: reactor.stop())

    signal.signal(signal.SIGINT, shutdown)

    with zk.connect(args.zk_addr, args.zk_timeout, args.zk_path):
        reactor.run()
