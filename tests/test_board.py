import unittest
from pathlib import Path

from pysudoku.board import Board
from pysudoku.exceptions import InvalidBoardFormatError

DATA = Path(__file__).parent / "data"


class TestBoard(unittest.TestCase):
    def test_compact_equals_spaced(self):

        """the dotted compact file parses to the same grid as the spaced one."""
        
        spaced = Board.from_file(DATA / "puzzle.txt")
        compact = Board.from_file(DATA / "puzzle_compact.txt")
        for r in range(9):
            for c in range(9):
                self.assertEqual(spaced.get(r, c), compact.get(r, c))

    def test_extra_five_conflicts(self):
        """(conflicts part): extra 5 gives the row 1 and box 2 messages."""

        board = Board.from_file(DATA / "puzzle_extra5.txt")

        self.assertEqual(board.find_conflicts(), [
            "Row 1: number 5 appears in columns 1 and 4.",
            "Box 2: number 5 appears at (1, 4) and (2, 6).",
        ])

    def test_eight_rows(self):
        """ a file with only 8 rows raises InvalidBoardFormatError."""
        with self.assertRaises(InvalidBoardFormatError):
            Board.from_file(DATA / "eight_rows.txt")

    def test_letter(self):
        """a row containing the letter x raises InvalidBoardFormatError."""
        with self.assertRaises(InvalidBoardFormatError):
            Board.from_file(DATA / "letter_x.txt")

    # extra tests 
    def test_valid_board_has_no_conflicts(self):
        self.assertEqual(Board.from_file(DATA / "puzzle.txt").find_conflicts(), [])

    def test_empty_cells_count(self):
        self.assertEqual(len(Board.from_file(DATA / "puzzle.txt").empty_cells()), 51)

    def test_copy_is_independent(self):
        board = Board.from_file(DATA / "puzzle.txt")
        clone = board.copy()
        clone.set(0, 2, 4)
        self.assertEqual(board.get(0, 2), 0)
        self.assertFalse(clone.is_given(0, 2))


if __name__ == "__main__":
    unittest.main()