from dataclasses import dataclass, field

from rx import typing


@dataclass
class TimeSync:
    source: typing.Observable[int] = field(repr=False)
    server_timestamp: int = field(default_factory=lambda: 0)

    def __post_init__(self):
        def update_time(timestamp: int):
            self.server_timestamp = timestamp

        self.source.subscribe(on_next=update_time)
