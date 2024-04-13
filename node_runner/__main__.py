
import argparse
import signal
import socket

from kazoo.client import KazooClient
from scrapy.utils.log import configure_logging
from twisted.internet import endpoints
from twisted.web import resource, server

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


if __name__ == '__main__':
    args = parse_args()

    zk = KazooClient(args.zk_addr)
    zk.start(timeout=1)

    reactor = get_reactor()

    executor = Executor()

    index = resource.Resource()
    index.putChild(b'start', Start(executor))

    site = server.Site(index)

    endpoint = endpoints.TCP4ServerEndpoint(reactor, args.port)
    endpoint.listen(site)

    def zk_create():
        zk.create(f'{args.zk_path}/{socket.gethostname()}', ephemeral=True, makepath=True)

    def shutdown(*_):
        d = executor.stop()
        d.addBoth(lambda _: reactor.stop())

    signal.signal(signal.SIGINT, shutdown)

    reactor.callInThread(zk_create)
    reactor.run()

    zk.stop()
    zk.close()
