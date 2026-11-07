import time
import unittest
from pathlib import Path

from pysudoku.board import Board
from pysudoku.exceptions import InvalidBoardError
from pysudoku.solver import Solver

DATA = Path(__file__).parent / "data"


def load(name: str) -> Board:
    return Board.from_file(DATA / name)


class TestSolver(unittest.TestCase):
    def test_case1_unique_solution(self):
        """
        Case 1: the sample puzzle has exactly one solution, the grid from the spec.
        """
        puzzle = load("puzzle.txt")
        solver = Solver(puzzle)
        self.assertEqual(solver.count_solutions(), 1)
        self.assertEqual(str(solver.solve()), str(load("solution.txt")))

    def test_case3_multiple_solutions(self):
        """
        Case 3: removing the 5 and 3 from row 1 makes the puzzle ambiguous.
        """
        self.assertEqual(Solver(load("multiple_solutions.txt")).count_solutions(), 2)

    def test_case4_valid_but_unsolvable(self):
        """
        Case 4: no rule is broken at the start, but there is no solution.
        """
        board = load("unsolvable.txt")
        self.assertEqual(board.find_conflicts(), [])
        solver = Solver(board)
        self.assertEqual(solver.count_solutions(), 0)
        self.assertIsNone(solver.solve())

    def test_case5_invalid_board_is_refused(self):
        """
        Case 5: a starting board with a duplicate raises InvalidBoardError.
        """
        with self.assertRaises(InvalidBoardError) as ctx:
            Solver(load("puzzle_extra5.txt"))
        self.assertEqual(ctx.exception.conflicts, [
            "Row 1: number 5 appears in columns 1 and 4.",
            "Box 2: number 5 appears at (1, 4) and (2, 6).",
        ])

    def test_case8_empty_board_is_fast(self):
        """
        Case 8: an empty board has MULTIPLE solutions, found in under a second.
        """
        start = time.perf_counter()
        count = Solver(load("empty_board.txt")).count_solutions()
        self.assertEqual(count, 2)
        self.assertLess(time.perf_counter() - start, 1.0)

    def test_case13_original_board_not_changed(self):
        """
        Case 13: solving works on a copy, so the original keeps its empty cells.
        """
        puzzle = load("puzzle.txt")
        before = str(puzzle)
        Solver(puzzle).solve()
        self.assertEqual(len(puzzle.empty_cells()), 51)
        self.assertEqual(str(puzzle), before)

    def test_count_stops_at_limit(self):
        """
        count_solutions never goes past the limit it was given.
        """
        solver = Solver(load("empty_board.txt"))
        self.assertEqual(solver.count_solutions(limit=3), 3)

    def test_solve_and_count_on_same_solver(self):
        """
        Calling solve() and then count_solutions() on one Solver is safe.
        """
        solver = Solver(load("puzzle.txt"))
        solver.solve()
        self.assertEqual(solver.count_solutions(), 1)


if __name__ == "__main__":
    unittest.main()
