from dataclasses import dataclass

from lightbulb import ResponseProxy


@dataclass
class ActivePoll:
    link: str
    name: str
    message: ResponseProxy
