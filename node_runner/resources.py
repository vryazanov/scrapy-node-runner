import datetime
import json

from twisted.web import resource
from twisted.web.http import Request

from node_runner.executor import Executor
from node_runner.exceptions import DuplicateError

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

class Active(resource.Resource):
    isLeaf = True

    def __init__(self, executor: Executor):
        self.executor = executor

    def render_POST(self, request):
        request.setHeader('Content-Type', 'application/json')
        executions = []
        for id, (crawler, started_at) in self.executor.active.items():
            duration = datetime.datetime.now(datetime.UTC) - started_at
            executions.append({
                'id': id,
                'stats': crawler.stats and crawler.stats.get_stats(),
                'duration': int(duration.total_seconds())
            })
        return json.dumps({'executions': executions}, default=serialize_datetime).encode()
