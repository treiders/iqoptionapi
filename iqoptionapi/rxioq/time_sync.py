from dataclasses import dataclass, field

from . import streamed_data


@dataclass
class TimeSync:
    server_timestamp: int = field(init=False)
    timestamp: streamed_data.From[int] = field(repr=False)

    def __post_init__(self):
        def update_me(value):
            self.timestamp.server_timestamp = value
        self.timestamp.subscribe(on_next=update_me)
