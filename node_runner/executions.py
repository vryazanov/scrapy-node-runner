import collections
import dataclasses
import datetime
import enum
import typing

from scrapy.crawler import Crawler


class Status(str, enum.Enum):
    running = 'running'
    terminating = 'terminating'
    stopped = 'stopped'
    finished = 'finished'


@dataclasses.dataclass
class Execution:
    id: str
    crawler: Crawler
    status: Status
    started_at: datetime.datetime
    finished_at: typing.Optional[datetime.datetime]

    @classmethod
    def create(cls, id: str, crawler: Crawler) -> 'Execution':
        return cls(
            id=id,
            crawler=crawler,
            status=Status.running,
            started_at=datetime.datetime.now(datetime.UTC),
            finished_at=None,
        )

    def duration(self) -> datetime.timedelta:
        return (self.finished_at or datetime.datetime.now(datetime.UTC))  - self.started_at

    def stop(self):
        self.status = Status.terminating
        self.crawler.stop()

    def finish(self):
        self.finished_at = datetime.datetime.now(datetime.UTC)

        if self.status == Status.terminating:
            self.status = Status.stopped
        elif self.status == Status.running:
            self.status = Status.finished
        else:
            raise RuntimeError('Unexpected status')


class Executions(collections.UserList):
    def __init__(self, data: typing.List[Execution]):
        self.data = data

    def active(self) -> typing.List[Execution]:
        return Executions([e for e in self.data if e.status == Status.running])

    def history(self) -> typing.List[Execution]:
        return Executions([e for e in self.data if e.status != Status.running])
