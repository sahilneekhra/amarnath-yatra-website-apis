from dataclasses import dataclass


@dataclass
class Availability:
    route: str
    date: str
    quota_text: str
    slots: int