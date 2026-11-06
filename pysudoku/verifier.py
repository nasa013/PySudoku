from dataclasses import dataclass, field
from .board import Board
from .solver import Solver

# a class to hold data and short for 
""" class VerificationReport:
    def __init__(self, status: str, problems: list[str]) -> None:
        self.status = status
        self.problems = problems

    def __repr__(self):
        return f"VerificationReport(status={self.status!r}, problems={self.problems!r})"

    def __eq__(self, other):
        return self.status == other.status and self.problems == other.problems
 """
@dataclass
class VerificationReport:
    status: str
    problems: list[str] = field(default_factory=list)


class Verifier:
    def __init__(self) -> None:
        pass