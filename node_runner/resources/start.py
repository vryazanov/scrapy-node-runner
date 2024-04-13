import json
import typing

from twisted.internet.defer import Deferred
from twisted.web import resource


class Executor(typing.Protocol):

    def start(self, id: str, project: str, spider: str, spider_args: dict) -> Deferred:
        ...


class Start(resource.Resource):
    isLeaf = True

    def __init__(self, executor: Executor):
        self.executor = executor

    def render_POST(self, request):
        data = json.loads(request.content.read())
        
        self.executor.start(
            data['id'],
            data['project'],
            data['spider'],
            data['spider_args'],
        )

        return b'{"success": true}'
