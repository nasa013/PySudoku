"""Solver: validates the board, solves it, and says whether it has 0, 1 or several solutions."""

from .board import Board
from .exceptions import InvalidBoardError


class Solver:
    """
    Solves a Board by backtracking. Never changes the board it was given
    """

    def __init__(self, board: Board) -> None:

        """
        Refuse an invalid board, then keep a private copy to work on
        """
        conflicts = board.find_conflicts()
        if conflicts:
            raise InvalidBoardError(conflicts)

        self._original = board.copy()   # never touched after this
        self._working = board.copy()    # the board the search fills and undoes
        self._found = 0                 # solutions counted so far

    def is_valid(self, r: int, c: int, num: int) -> bool:
        """
        Return True if num can be placed at (r, c) without clashing
        
        """
        # row
        for col in range(9):
            if self._working.get(r, col) == num:
                return False

        # column
        for row in range(9):
            if self._working.get(row, c) == num:
                return False

        # 3x3 box
        box_r = (r // 3) * 3
        box_c = (c // 3) * 3
        for row in range(box_r, box_r + 3):
            for col in range(box_c, box_c + 3):
                if self._working.get(row, col) == num:
                    return False

        return True

    def backtracking(self) -> bool:
        """
        Fill empty cells one by one. Return True when the board is complete
        """
        empty = self._working.empty_cells()

        # base case: no empty cell left, so it is solved
        if not empty:
            return True

        # select a cell
        r, c = empty[0]

        # try each digit
        for num in range(1, 10):
            if self.is_valid(r, c, num):
                self._working.set(r, c, num)      # try it

                if self.backtracking():           # recurse
                    return True

                self._working.set(r, c, 0)        # undo (the backtrack)

        # no digit worked: tell the caller to undo its choice
        return False

    def solve(self) -> Board | None:
        """
        Return the solved board, or None if the puzzle has no solution
        """
        self._working = self._original.copy()     # always start from the clean puzzle

        if self.backtracking():
            return self._working.copy()

        return None

    def _count_search(self, limit: int) -> bool:
        """
        Same search as backtracking, but keeps counting until `limit` solutions are found
        """
        empty = self._working.empty_cells()

        if not empty:                             # a full valid board = one solution
            self._found += 1
            return self._found >= limit           # True only when we have enough

        r, c = empty[0]
        for num in range(1, 10):
            if self.is_valid(r, c, num):
                self._working.set(r, c, num)
                if self._count_search(limit):     # limit reached: stop everything
                    return True
                self._working.set(r, c, 0)        # undo and keep searching for MORE solutions
        return False

    def count_solutions(self, limit: int = 2) -> int:
        """
        Count solutions, stopping as soon as `limit` of them are found
        """
        self._working = self._original.copy()
        self._found = 0
        self._count_search(limit)
        return self._found