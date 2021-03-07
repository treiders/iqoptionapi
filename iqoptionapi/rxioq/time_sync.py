from dataclasses import dataclass, field

from . import streamed_data


@dataclass
class TimeSync:
    server_timestamp: streamed_data.From[int]
