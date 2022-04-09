from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class RateLimit:
    """`limit` calls per `limit_time_interval` seconds"""

    limit: int
    limit_time_interval: int

    def __str__(self) -> str:
        return f"{self.limit} calls / {self.limit_time_interval}s"
