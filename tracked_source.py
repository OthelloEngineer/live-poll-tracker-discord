from dataclasses import dataclass

from lightbulb import ResponseProxy


@dataclass
class TrackedSource:
    link: str
    name: str
    message: ResponseProxy
