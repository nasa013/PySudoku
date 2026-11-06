"""
Read the original puzzle and the player's grid (same file format), then report every problem in this order:

1. Given cells changed: a cell that was non-zero in the puzzle has a different value in the submission.
2. Empty cells: any `0` or `.` left in the submission.
3. Duplicates: a digit repeated in a row, a column or a box, each reported once per row/column/box.

The final status is:

- `VALID SOLUTION` — no problems at all;
- `INCOMPLETE` — only empty cells, no rule broken so far;
- `INVALID SOLUTION` — at least one changed given or duplicate.

A submission that keeps every given, has no empty cells and no duplicates **is** a correct solution by definition. You do not need to compare it with your solver's answer.

"""





from dataclasses import dataclass, field
from .board import Board
from .solver import Solver

'''
Compares a player's grid with the puzzle and lists every mistake

'''

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
    def __init__(self , puzzle : Board , submision : Board ) -> None:
        self._puzzle = puzzle
        self._submision = submision

    def verify(self):

        changed_givens: list[str] = []
        empty_cells: list[str] = []



        for r in range(9):
            for c in range(9):
                value = self._submision.get(r, c)

                # givens is changed 
                if self._puzzle.is_given(r,c):
                    org= self._puzzle.get(r,c)
                    if value != org:
                        changed_givens.append(
                            f"Row {r + 1}, Column {c + 1}: value {value} "
                            f"overwrites the given number {org}."
                        )


                # empty cells
                if value == 0 or value == "." :
                    empty_cells.append(f"Row {r + 1}, Column {c + 1}: cell is empty.")


        # check duplicates 
        duplicates = self._submision.find_conflicts()

        problems = changed_givens + empty_cells + duplicates 

        if not problems:
            status = "VALID SOLUTION"
        elif not changed_givens and not duplicates:
            status = "INCOMPLETE"          # only empty cells
        else:
            status = "INVALID SOLUTION"

        return VerificationReport(status=status , problems= problems)



                
                    
    
