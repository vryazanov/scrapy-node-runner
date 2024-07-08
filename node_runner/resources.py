import datetime
import json

from twisted.web import resource
from twisted.web.http import Request
from scrapy.settings import Settings

from node_runner.exceptions import DuplicateError
from node_runner.executions import Execution, Executions
from node_runner.executor import Executor


def serialize_datetime(obj): 
    if isinstance(obj, datetime.datetime): 
        return obj.isoformat() 
    raise TypeError("Type not serializable") 


class Start(resource.Resource):
    isLeaf = True

    def __init__(self, executor: Executor):
        self.executor = executor

    def render_POST(self, request: Request):
        request.setHeader('Content-Type', 'application/json')
        data = json.loads(request.content.read())
        
        success = True

        try:
            self.executor.schedule(
                data['id'],
                data['spider'],
            )
        except DuplicateError:
            success = False

        return json.dumps({'success': success}).encode()


class Stop(resource.Resource):
    isLeaf = True

    def __init__(self, executor: Executor):
        self.executor = executor

    def render_POST(self, request):
        request.setHeader('Content-Type', 'application/json')
        data = json.loads(request.content.read())
        
        self.executor.stop(
            data['id'],
        )

        return b'{"success": true}'


def render_execution(execution: Execution) -> dict:
    return {
        'id': execution.id,
        'spider': execution.crawler.spider.name,
        'status': execution.status,
        'stats': execution.crawler.stats.get_stats(),
        'duration': int(execution.duration().total_seconds()),
    }


class Active(resource.Resource):
    isLeaf = True

    def __init__(self, executions: Executions):
        self.executions = executions

    def render_POST(self, request):
        request.setHeader('Content-Type', 'application/json')

        return json.dumps({'executions': [
            render_execution(execution)
            for execution in self.executions.active()
        ]}, default=serialize_datetime).encode()


class History(resource.Resource):
    isLeaf = True

    def __init__(self, executions: Executions):
        self.executions = executions

    def render_POST(self, request):
        request.setHeader('Content-Type', 'application/json')

        return json.dumps({'executions': [
            render_execution(execution)
            for execution in self.executions.history()
        ]}, default=serialize_datetime).encode()


class Meta(resource.Resource):
    isLeaf = True

    def __init__(self, settings: Settings):
        self.settings = settings

    def render_POST(self, request):
        request.setHeader('Content-Type', 'application/json')

        return json.dumps({
            'project_name': self.settings.get('BOT_NAME'),
        }).encode()
