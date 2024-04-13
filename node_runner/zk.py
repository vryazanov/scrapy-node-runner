import contextlib
import socket

from kazoo.client import KazooClient


@contextlib.contextmanager
def connect(addr: str, timeout: int, path: str):
    zk = KazooClient(addr)
    zk.start(timeout=timeout)
    zk.create(f'{path}/{socket.gethostname()}', ephemeral=True, makepath=True)

    yield

    zk.stop()
    zk.close()
