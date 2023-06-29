from dataclasses import dataclass


@dataclass
class PollData:
    reference_name: str
    question: str
    options: dict[str, int]
    total_votes: int
    link: str

    def __repr__(self):
        return f"question={self.question}, \n options={self.options}, \n " \
               f"total_votes={self.total_votes}, \n link={self.link}"
