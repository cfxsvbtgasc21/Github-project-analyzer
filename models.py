from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Commit:
    sha: str
    author: str
    date: datetime
    message: str

@dataclass
class Repository:
    name: str
    owner: str
    stars: int
    forks: int
    commits: List[Commit]
    contributors: List[str] 