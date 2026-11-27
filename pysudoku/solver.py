"""Solver: validates the board, solves it, and says whether it has 0, 1 or several solutions."""

from .board import Board
from .exceptions import InvalidBoardError


class Solver:
    """
    Solves a Board by backtracking. Never changes the board it was given
    """

    def __init__(self, board: Board , use_mrv : bool = True) -> None:

        """
        Refuse an invalid board, then keep a private copy to work on
        use_mrv: pick the most constrained cell first (default True)
        """
        conflicts = board.find_conflicts()
        if conflicts:
            raise InvalidBoardError(conflicts)

        self._original = board.copy()   # never touched after this
        self._working = board.copy()    # the board the search fills and undoes
        self._found = 0                 # solutions counted so far

        # MRV 
        self._use_mrv = use_mrv
        self.calls = 0


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

# updated for mrv
    def backtracking(self) -> bool:
        """
        Fill empty cells one by one. Return True when the board is complete
        """
       
        self.calls += 1

        cell = self._pick_cell()

        # base case: no empty cell left, so it is solved
        if cell is None:
            return True

        r , c , options = cell

        # try only the options
        for num in options:
            self._working.set(r, c, num)

            if self.backtracking():
                return True

            self._working.set(r, c, 0)  # undo

        return False

    def solve(self) -> Board | None:
        """
        Return the solved board, or None if the puzzle has no solution
        """
        self.calls = 0
        self._working = self._original.copy()     # always start from the clean puzzle

        if self.backtracking():
            return self._working.copy()

        return None

    def _count_search(self, limit: int) -> bool:
        """
        Same search as backtracking, but keeps counting until `limit` solutions are found
        """
        
        self.calls += 1

        cell = self._pick_cell()


        # Base .. one solution
        if cell is None:
            self._found += 1
            return self._found >= limit

        r, c, options = cell

        for num in options:
            self._working.set(r, c, num)

            if self._count_search(limit):
                return True  # limit reached: stop searching

            self._working.set(r, c, 0)  # undo and keep searching

        return False

    def count_solutions(self, limit: int = 2) -> int:
        """
        Count solutions, stopping as soon as `limit` of them are found
        """
        self.calls = 0 

        self._working = self._original.copy()
        self._found = 0
        self._count_search(limit)
        return self._found

    # MRV 
    def _options(self , r : int , c: int) -> list[int] :
        '''
        see all the possible options  from 1 to 9 are allowed to go in this cell right now
        '''
        result = []

        for n in range(1, 10):
            if self.is_valid(r, c, n):
                result.append(n)

        return result

    def _pick_cell(self) -> tuple[int, int, list[int]] | None:
        """
        choose the empty cell with the fewest candidates
        """

        empty = self._working.empty_cells()

        if not empty:
            return None

        # If MRV is disabled, choose the first empty cell
        if not self._use_mrv:
            r, c = empty[0]
            return r, c, self._options(r, c)

        best = None

        for r, c in empty:
            cands = self._options(r, c)

            if best is None or len(cands) < len(best[2]):
                best = (r, c, cands)

        return best